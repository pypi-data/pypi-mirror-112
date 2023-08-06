# neo-mp-loader

res:
redis
graphio
jsonpickle



STATUS:

YOU ARE DEMO 3. with the subset there is drain order left in the cache in the end. thats maybe the reason the bigger testset is looping in the end
# Strategies

* Seperated Datasets
    + Nodes and Relations are not interconnected to other datasets/workers
    + We can just run the relations after the nodes are created/merged
* Capsuled Datasets
    + Nodes and Relations are in one dataset, but nodes between datasets can overlap when merged
    + We need to make sure that the two nodeSets between a RelSet, and the RelSet itself, is in a stable status (=only finished workers discharged in these nodesets and the relset. no currently running worker are allowed to discharge in these nodeset and the relset) before loading the relations
* Mixed Datasets
    + Nodes and Relations are scattered over multiple datasets/workers.
    + We first need to load all nodes before loading relations.
    + this could blast memory on large loading runs. any ideas? maybe an emergency discharge to disk if relations are eating too much memory? quite complex...


# Issues

* Make sure that new related NodeSetLoading workers are blocked if a RelationshipSetLoading Worker is waiting for a drain and/or loading. otherwise we could provoke nodelocks

* Tidy up:_
    * Finished Drain orders should remove  entries from "DRAIN_ORDERS_NODESETS_DONE"
    * Finished Drain orders can be removed from "DRAIN_ORDERS_READY"
    * Remove unnessecary drain state "DRAIN_ORDERS_FIN_KEY"

# ToDo


* Loading worker shoud get trigger if a min amount of data is in cache (as long as there a still sourcing workers pumping data)
* Docu
* replace redis-py with aioredis