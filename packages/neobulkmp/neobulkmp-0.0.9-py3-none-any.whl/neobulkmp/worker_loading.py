from logging import raiseExceptions
import graphio
import traceback
from py2neo import Graph
from typing import Dict
from .worker_base import WorkerBase
from .cache_backend import CacheInterface, SetsMetaBase


class WorkerLoading(WorkerBase):
    def __init__(
        self,
        name,
        set_meta: SetsMetaBase,
        graph_params: Dict,
        insert_action: str = "create",
        create_index: bool = True,
        create_unique_constraints: bool = False,
    ):
        super(type(self), self).__init__()
        self.name: str = name
        self.set_meta: SetsMetaBase = set_meta
        self.graph_params: Dict = graph_params
        self.insert_action: str = insert_action
        self.create_index = create_index
        self.create_unique_constraints = create_unique_constraints
        self.drain_order_ticket = None

    def run(self):
        super(type(self), self).run()
        self.cache: CacheInterface = self.cache_backend(self.cache_backend_params)
        graph_set = None
        log = self.get_logger()
        log.info(f"START {self.name}")
        try:
            if self.set_meta.type == graphio.NodeSet:
                graph_set = self.cache.fetch_NodeSets(self.set_meta)
            elif self.set_meta.type == graphio.RelationshipSet:
                graph_set = self.cache.fetch_RelSets(
                    self.set_meta, self.drain_order_ticket
                )
            else:
                log.error(
                    f"Wrong meta data for set. Expected <graphio.NodeSet> or <graphio.RelationshipSet> got {self.set_meta.type}"
                )
                raise ValueError(
                    f"Wrong meta data for set. Expected <graphio.NodeSet> or <graphio.RelationshipSet> got {self.set_meta.type}"
                )
        except Exception as e:
            log.error(traceback.format_exc())
            raise e
        try:
            g = Graph(**self.graph_params)

            if self.create_index:
                log.debug(f"Create index for {graph_set}")
                graph_set.create_index(g)
            if self.create_unique_constraints:
                log.debug(f"Create unique constraint for {graph_set}")
                raise NotImplementedError
            if self.insert_action == "create":
                log.debug(f"Load into DB with 'create' {graph_set}")
                graph_set.create(g)
            elif self.insert_action == "merge":
                log.info(f"Load into DB with 'merge' {graph_set}")
                graph_set.merge(g)
            else:
                m = f"Unknown insert action. Expected 'create' or 'merge' got '{self.insert_action}'"
                log.error(m)
                raise ValueError(m)
        except Exception as e:
            log.exception(f"Failed to insert {self.set_meta}")
            raise e
        self.cache.report_SetLoaded(graph_set)
        log.info(f"Finished")
