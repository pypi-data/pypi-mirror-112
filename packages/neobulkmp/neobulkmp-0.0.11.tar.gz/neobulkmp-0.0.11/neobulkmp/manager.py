import multiprocessing
import logging
from multiprocessing.context import ProcessError
import operator
import graphio
import json
import time
from linetimer import CodeTimer
from typing import List, Dict, Type, Set, Union, Tuple
from .worker_base import WorkerBase
from .worker_sourcing import WorkerSourcing
from .worker_loading import WorkerLoading
from .cache_backend import (
    CacheInterface,
    NodeSetMeta,
    RedisCache,
    RelationSetMeta,
    SetsMetaBase,
)
from .manager_strategies import StrategyBase
from .cache_logger import LogRecordStreamHandler
import humanfriendly

log = logging.getLogger(__name__)


class Manager:
    # Redis - Default cache backend

    strategy_type: Type[StrategyBase] = StrategyBase

    def __init__(
        self,
        worker_sourcing_class: Type[WorkerSourcing],
        worker_parameters: List[Dict],
        cache_backend: Type[CacheInterface] = RedisCache,
        cache_backend_params: Dict = None,
        cache_size: str = "500MB",
    ):
        """[summary]

        Args:
            worker_sourcing_class (Type[WorkerSourcing]): [description]
            worker_parameters (List[Dict]): [description]
            cache_backend (Type[CacheInterface], optional): [description]. Defaults to RedisCache.
            cache_backend_params (Dict, optional): [description]. Defaults to None.
            cache_size (str, optional): Max size of cache that should be available in humanfriendly ( https://pypi.org/project/humanfriendly/ ) format . Defaults to "500MB".
        """
        self.worker_sourcing_class = worker_sourcing_class
        self.worker_parameters = worker_parameters
        self.worker_loading_class = WorkerLoading
        self.graph_params = {}
        self.cpu_count: int = multiprocessing.cpu_count()
        self.max_concurrently_worker_count = self.cpu_count - 1
        self.max_source_workers_count = self.max_concurrently_worker_count
        self.cancel_on_source_worker_failed = False
        self.cache_backend = cache_backend
        self.cache_backend_params = cache_backend_params
        self.cache = self.cache_backend(self.cache_backend_params)
        self.strategy: StrategyBase = self.strategy_type(self)
        self.insert_action: str = "create"
        self.create_indexes = True
        self.create_unique_constraints = False
        self.worker_logging_reciever = LogRecordStreamHandler(self.cache)
        self.cache_size = humanfriendly.parse_size(cache_size)

        self._blocked_nodesets: Dict[str, Set[SetsMetaBase]] = {}

    def test_cache_backend_ready(self):
        if self.cache.test_connection():
            return True
        else:
            return False

    def is_cache_log_flushed(self):
        if len(self.cache.get_logs()) == 0:
            return True
        else:
            return False

    def merge(self, graph_params: Dict = {}):
        self.graph_params = graph_params
        self.insert_action = "merge"
        self._start()

    def create(self, graph_params: Dict = {}):
        self.graph_params = graph_params
        self.insert_action = "create"
        self._start()

    def _start(self):
        if not self.test_cache_backend_ready():
            raise Exception(
                f"Cache backend {type(self.cache_backend)} {self.cache_backend_params} not available!"
            )
        self.manager_sourcing = ManagerWorkersSourcing(self, self.worker_sourcing_class)
        self.manager_loading = ManagerWorkersLoading(self, self.worker_loading_class)
        finished = False
        self.worker_logging_reciever.handle()
        log.info("##Management start##")
        while not finished:
            log.debug(f"_blocked_nodesets: {self._blocked_nodesets}")
            self.manager_sourcing.manage()
            self.manager_loading.manage()
            finished = (
                self.manager_sourcing.is_done() and self.manager_loading.is_done()
            )
            # Wait for next management tick
            time.sleep(0.05)
            # finished = self.manager_sourcing.is_done()
        log.info("##Management finish##")
        # Wait for all log records to be processed
        while not self.is_cache_log_flushed():
            time.sleep(0.3)

    def _block_loading_nodeset_type(self, block_id: str, nodeset_meta: SetsMetaBase):
        if block_id in self._blocked_nodesets:
            self._blocked_nodesets[block_id].add(nodeset_meta)
        else:
            self._blocked_nodesets[block_id] = {nodeset_meta}

    def _release_nodeset_type_loading_block(self, block_id):
        self._blocked_nodesets.pop(block_id, None)

    def _get_blocked_nodeset_types(self) -> List[SetsMetaBase]:
        # flatten all values in a list and remove duplicates
        return list(
            {val for val_list in self._blocked_nodesets.values() for val in val_list}
        )


class ManagerWorkersBase:
    parent: Manager = None
    worker_class: Type[WorkerBase] = None

    def __init__(self, manager: "Manager", worker_class: Type[WorkerBase]):
        self.parent = manager
        self.workers: List[WorkerBase] = []
        self.finished_workers: List[WorkerBase] = []
        self.failed_workers: List[WorkerBase] = []
        self.worker_class = worker_class

        # Setup caching backend on worker class

        self.worker_class.cache_backend = self.parent.cache_backend
        self.worker_class.cache_backend_params = self.parent.cache_backend_params

    def is_done(self):
        raise NotImplementedError

    def _get_process_status(self, worker):
        if worker.is_alive():
            return "running"
        else:
            if worker.exitcode is None:
                return "initial"
            elif worker.exitcode == 0 and worker not in self.finished_workers:
                return "exited"
            elif worker.exitcode != 0 and worker not in self.failed_workers:
                return "failed"
            elif worker in self.finished_workers + self.failed_workers:
                return "finished"
        raise ValueError(
            "Could not determine process status. Something went wrong",
            worker.exitcode,
            worker,
        )

    def _get_cache_sets_meta_data(
        self, sort_attr="total_size_bytes", set_type=None
    ) -> List[SetsMetaBase]:
        meta_data = self.parent.cache.list_SetsMeta(set_type=set_type)
        return meta_data

    def _init_workers(
        self, parameters: List[Dict], names: List[str] = None, tags: List = None
    ):
        if not names:
            names = [hash(str(p)) for p in parameters]
        for name, params in zip(names, parameters):
            name = f"{self.worker_class.__name__}-{';'.join(tags or [])}-{name}"
            w: WorkerBase = self.worker_class(name=name, **params)
            log.info(f"INIT WORKER {w.name}")
            w.tags = tags
            w.params = params
            self.workers.append(w)

    def _finish_workers(self, tag: str = None) -> bool:
        did_any_workers_finish = False
        for fin_worker in self._get_workers("exited", tag=tag):
            did_any_workers_finish = True
            fin_worker.join()
            fin_worker.timer.__exit__(None, None, None)
            self.parent._release_nodeset_type_loading_block(fin_worker.id)
            fin_worker.progress = "finished"
            self.finished_workers.append(fin_worker)

            log.debug(f"Exit worker '{fin_worker.name}'")
        # Exit failed worker
        for fail_worker in self._get_workers("failed", tag=tag):
            did_any_workers_finish = True
            fail_worker.join()
            fail_worker.timer.__exit__(None, None, None)
            # release any nodeset blocks
            self.parent._blocked_nodesets.pop(fail_worker.id, None)
            self.failed_workers.append(fail_worker)
            fin_worker.progress = "finished"
            log.error(
                f"Exit failed worker '{fail_worker.name}' \n other workers currently running are {self._get_workers('running')}"
            )
            raise ProcessError(f"'{fail_worker.name}' failed")
        return did_any_workers_finish

    def _get_workers(
        self,
        status: Union[str, List, Tuple, Set] = None,
        progress: Union[str, List, Tuple, Set] = None,
        tag=None,
    ):
        return [
            w
            for w in self.workers
            if (tag is None or tag in w.tags)
            and (
                status is None
                or (isinstance(status, str) and self._get_process_status(w) == status)
                or (
                    isinstance(status, (list, set, tuple))
                    and self._get_process_status(w) in status
                )
            )
            and (
                progress is None
                or (isinstance(progress, str) and w.progress == progress)
                or (isinstance(progress, (list, set, tuple)) and w.progress in progress)
            )
        ]


class ManagerWorkersSourcing(ManagerWorkersBase):
    def __init__(self, manager: "Manager", worker_class: Type[WorkerBase]):
        super(type(self), self).__init__(manager, worker_class)
        # create workers distribute task parameters per worker
        log.debug(f"self.parent.worker_parameters: {self.parent.worker_parameters}")
        self._init_workers(parameters=self.parent.worker_parameters)
        self.worker_count_total = len(self.workers)

    def is_done(self):
        # Mom, Are We There Yet?
        if len(self.workers) == len(self.finished_workers) + len(self.failed_workers):
            return True
        else:
            return False

    def manage(self):
        available_cores = self.parent.strategy.amount_sourcing_cores()
        # Collect all running sourcing workers
        waiting_workers = self._get_workers("initial")
        new_worker_started = False
        # Start next worker
        if (
            len(self._get_workers("running")) < available_cores
            and len(waiting_workers) > 0
        ):
            new_worker_started = True
            next_worker = waiting_workers.pop(0)
            log.debug(f"CALL START ON SOURCING {next_worker} - {next_worker.params}")
            next_worker.start()
            next_worker.timer.__enter__()

        workers_did_finished = self._finish_workers()
        if workers_did_finished or new_worker_started:
            log.debug(
                f"SOURCING: {len(self.finished_workers) + len(self.failed_workers)} Workers finished / {len(self._get_workers('running'))} Workers running / {len(self._get_workers('initial'))} Workers waiting / {len(self.failed_workers)} Workers failed / {available_cores} Max sourcing workers running simultaneously"
            )


class ManagerWorkersLoading(ManagerWorkersBase):
    def __init__(self, manager: "Manager", worker_class: Type[WorkerBase]):
        super(type(self), self).__init__(manager, worker_class)
        self.parent = manager
        self.drain_waiting_workers: List[WorkerLoading] = []
        self.drain_ready_workers: List[WorkerLoading] = []
        self.loading_workers: List[WorkerLoading] = []
        self.exited_workers: List[WorkerLoading] = []
        self.failed_workers: List[WorkerLoading] = []

        # Setup caching backend on worker class
        self.parent.worker_loading_class.cache_backend = self.parent.cache_backend
        self.parent.worker_loading_class.cache_backend_params = (
            self.parent.cache_backend_params
        )
        self.worker_tag_relsets = "RELSET"
        self.worker_tag_nodesets = "NODESET"

    def is_done(self):
        # we are done when:
        # sourcing is finished and there is no more data in the cache...
        if (
            self.parent.manager_sourcing.is_done()
            and not self._get_cache_sets_meta_data()
        ):
            # ... and all workers are finished
            if (
                len(self._get_workers("running")) + len(self._get_workers("initial"))
                == 0
            ):
                return True
        else:
            return False

    def manage_nodeset_loading(self, assigned_no_of_cores):
        log.info(
            f"Manage Nodesets loading with {assigned_no_of_cores} cores available and {len(self._get_workers('running',tag=self.worker_tag_nodesets))} worker running atm"
        )
        cached_sets = self._get_cache_sets_meta_data(set_type=graphio.NodeSet)

        # find NodeSets that have workers assigned (allready running or queued)
        cached_sets_worked_on: List[SetsMetaBase] = [
            cs
            for cs in cached_sets
            if cs
            in [
                worker.set_meta
                for worker in self._get_workers(
                    progress=("initial", "loading"), tag=self.worker_tag_nodesets
                )
            ]
        ]
        # find nodeSets types that are not loaded atm
        cached_sets_not_worked_on: List[SetsMetaBase] = [
            cs for cs in cached_sets if cs not in cached_sets_worked_on
        ]
        # find nodeSets that are blocked (because a related relationShip type is loaded atm)
        cache_sets_blocked = self.parent._get_blocked_nodeset_types()
        # Collect nodeSets that are not allready loaded and that are not blocked. These are the NodeSets type we can tackle next
        cached_sets_not_worked_on_and_not_blocked: List[SetsMetaBase] = [
            cs for cs in cached_sets_not_worked_on if cs not in cache_sets_blocked
        ]
        if cached_sets_not_worked_on_and_not_blocked:
            # Prepare parameter to initialize workers
            workers_params: List[Dict] = [
                {
                    "set_meta": cached_set_meta,
                    "graph_params": self.parent.graph_params,
                    "insert_action": self.parent.insert_action,
                    "create_index": self.parent.create_indexes,
                    "create_unique_constraints": self.parent.create_unique_constraints,
                }
                for cached_set_meta in cached_sets_not_worked_on_and_not_blocked
            ]
            # generate human readable names for workers
            worker_names: List[str] = [
                ":".join(self.parent.cache.get_NodeSetMeta(cached_set_meta).labels)
                for cached_set_meta in cached_sets_not_worked_on_and_not_blocked
            ]
            # Initialize workers
            self._init_workers(
                parameters=workers_params,
                names=worker_names,
                tags=[self.worker_tag_nodesets],
            )
        no_of_free_cores = assigned_no_of_cores - len(
            self._get_workers("running", tag=self.worker_tag_nodesets)
        )

        new_worker_started = False
        log.info(f"no_of_free_cores: {no_of_free_cores}")
        if no_of_free_cores > 0:
            # start one new worker
            for next_worker in self._get_workers(
                progress="initial", tag=self.worker_tag_nodesets
            )[:1]:
                new_worker_started = True
                next_worker.progress = "loading"
                next_worker.timer.__enter__()
                next_worker.start()

        # collect exited workers
        workers_did_finished = self._finish_workers(self.worker_tag_nodesets)
        if workers_did_finished or new_worker_started:
            log.debug(
                f"LOADING-NODESETS: {len(self.finished_workers) + len(self.failed_workers)} Workers finished / {len(self._get_workers('running'))} Workers running / {len(self._get_workers('initial'))} Workers waiting / {len(self.failed_workers)} Workers failed / {assigned_no_of_cores} Max sourcing workers running simultaneously"
            )

    def manage_relation_loading(self, assigned_no_of_cores):
        log.info(
            f"Manage Relsets loading with {assigned_no_of_cores} cores available and {len(self._get_workers('running',tag=self.worker_tag_relsets))} worker running atm"
        )
        cached_sets = self._get_cache_sets_meta_data(set_type=graphio.RelationshipSet)

        # find RelSets that have workers assigned (allready running or queued)
        cached_sets_worked_on: List[SetsMetaBase] = [
            cs
            for cs in cached_sets
            if cs
            in [
                worker.set_meta
                for worker in self._get_workers(
                    progress=("initial", "drain_ordered", "drain_ready", "loading"),
                    tag=self.worker_tag_relsets,
                )
            ]
        ]

        log.info(f"Relations cached_sets_worked_on count: {len(cached_sets_worked_on)}")
        if not len(cached_sets_worked_on) >= assigned_no_of_cores:
            cached_sets_not_worked_on: List[RelationSetMeta] = [
                self.parent.cache.get_RelSetMeta(cs)
                for cs in cached_sets
                if cs not in cached_sets_worked_on
            ]

            if cached_sets_not_worked_on:
                # Prepare parameter and name list to initialize new workers
                workers_params: List[Dict] = [
                    {
                        "set_meta": cached_set_meta,
                        "graph_params": self.parent.graph_params,
                        "insert_action": self.parent.insert_action,
                        "create_index": self.parent.create_indexes,
                        "create_unique_constraints": self.parent.create_unique_constraints,
                    }
                    for cached_set_meta in cached_sets_not_worked_on
                ]
                # generate human readable names for workers
                worker_names: List[str] = []
                for cached_set_meta in cached_sets_not_worked_on:
                    worker_names.append(cached_set_meta.rel_type)
                # Initialize workers
                self._init_workers(
                    parameters=workers_params,
                    names=worker_names,
                    tags=[self.worker_tag_relsets],
                )
        no_of_free_cores = assigned_no_of_cores - len(
            self._get_workers("running", tag=self.worker_tag_relsets)
        )

        # manage drain orders
        self._order_drains(assigned_no_of_cores)
        log.info(f"relsets free cores: {no_of_free_cores}")
        new_worker_started = False
        if no_of_free_cores > 0:
            # start one new worker
            for next_worker in self._get_workers(
                progress="drain_ready", tag=self.worker_tag_relsets
            ):
                # check if there is not another relationship set loader  at the moment which has a intersection at the target nodesets
                if self._find_running_relset_worker_with_same_target_nodesets(
                    next_worker
                ):
                    #    # there is another worker working on the same nodeset as the potential next_worker. we skip this round and go to the next potential worker
                    continue
                new_worker_started = True
                next_worker.progress = "loading"
                next_worker.timer.__enter__()
                log.info(f"Start {next_worker.name}")
                next_worker.start()
                # we break the loop here as we only start one relationshipSet loader per management tick
                break

        # collect exited workers
        workers_did_finished = self._finish_workers(self.worker_tag_relsets)
        if workers_did_finished or new_worker_started:
            log.debug(
                f"LOADING-GRAPH: {len(self.finished_workers) + len(self.failed_workers)} Workers finished / {len(self._get_workers('running'))} Workers running / {len(self._get_workers('initial'))} Workers waiting / {len(self.failed_workers)} Workers failed / {assigned_no_of_cores} Max sourcing workers running simultaneously"
            )

    def _find_running_relset_worker_with_same_target_nodesets(self, worker):
        my_nodesets = worker.set_meta.target_nodeSets
        for other_relset_worker in [
            other_w
            for other_w in self._get_workers("running", tag=self.worker_tag_relsets)
            if other_w != worker
        ]:
            other_nodesets = other_relset_worker.set_meta.target_nodeSets
            for o_ns in other_nodesets:
                if o_ns in my_nodesets:
                    return other_relset_worker
        return None

    def _order_drains(self, assigned_no_of_cores):

        # Order drain for relationsSet attached NodeSets for next waiting worker

        # if there are allready some drains ordered we dont want to clog the line further
        # idle_drain_orders = self.drain_waiting_workers + self.drain_ready_workers
        # if len(idle_drain_orders) >= assigned_no_of_cores:
        #    return

        next_workers = [
            w
            for w in self._get_workers(progress="initial", tag=self.worker_tag_relsets)
            # if w not in self.drain_waiting_workers and w not in self.drain_ready_workers
        ]
        for next_worker in next_workers[:1]:
            drain_order_ticket_id = self.parent.cache.order_RelSetDrain(
                relset_meta=next_worker.set_meta
            )
            next_worker.progress = "drain_ordered"
            next_worker.drain_order_ticket = drain_order_ticket_id
            self.drain_waiting_workers.append(next_worker)

        # Check if any running drains are ready
        # tmp_drain_waiting_workers = []
        for drain_wait_worker in self._get_workers(
            progress="drain_ordered", tag=self.worker_tag_relsets
        ):
            drains_done = True
            if not self.parent.cache.is_drain_done(
                drain_wait_worker.drain_order_ticket
            ):
                drains_done = False
                #### tmp_drain_waiting_workers.append(drain_wait_worker)

                # The drain is still running. we cant do anything atm
                continue
            relset_meta_details: SetsMetaBase = self.parent.cache.get_RelSetMeta(
                drain_wait_worker.set_meta
            )
            # if drain is done: now we need to block new workers on our nodesets type and wait for running workers, that are loading our target nodeset types, to finish
            if drains_done:
                for nodeset in relset_meta_details.target_nodeSets:
                    self.parent._block_loading_nodeset_type(
                        drain_wait_worker.id, nodeset
                    )
            # It can happen that workers, which were started before the drain order and are loading nodesets that are related to the relationshipSet, are still loading.
            # this means: there could be nodelocks when loading the relationshipSet or worse target nodes could be missing.
            # We need to make sure that there are no old running workers
            nodesets_currently_worked_on: List[SetsMetaBase] = [
                worker.set_meta
                for worker in self._get_workers(
                    progress=("initial", "loading"),
                    tag=self.worker_tag_nodesets,
                )
            ]

            log.info(
                f"nodesets_currently_worked_on count: {len(nodesets_currently_worked_on)}"
            )

            for nodeset in relset_meta_details.target_nodeSets:
                if nodeset in nodesets_currently_worked_on:
                    # reverse decision, because nodeset type is still loaded by another worker
                    drains_done = False
                    ####tmp_drain_waiting_workers.append(drain_wait_worker)
            # END FIX EDGECASE
            if drains_done:
                log.info(
                    f"DRAIN SEEMS FINISHED drain_wait_worker.drain_order_ticket: {drain_wait_worker.drain_order_ticket}"
                )
                drain_wait_worker.progress = "drain_ready"
                #### if drain_wait_worker not in self.drain_ready_workers:
                ####    self.drain_ready_workers.append(drain_wait_worker)
        #### self.drain_waiting_workers = list(set(tmp_drain_waiting_workers))

    def manage(self):
        c = round(self.parent.strategy.amount_loading_cores() * 0.6)
        self.manage_nodeset_loading(assigned_no_of_cores=c if c > 0 else 1)
        c = round(self.parent.strategy.amount_loading_cores() * 0.4)
        self.manage_relation_loading(assigned_no_of_cores=c if c > 0 else 1)
