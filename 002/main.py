# Demo usage of persisting task results
# Each task result will be stored in a serialized form to disk

import numpy as np
import prefect
from prefect import task, Flow
from prefect import context as prectx
from prefect.engine.results import LocalResult

import cloudpickle

# NOTE: Only works if env variable is set!
# export PREFECT__FLOWS__CHECKPOINTING=true

#@task(result=LocalResult(dir='./localtask'))
@task
def sum(a, b):
    logger = prectx.get("logger")
    c = a + b
    logger.info(f"Result: {c}")
    return c


def example():
    with Flow('Example 002', result=LocalResult(dir='./checkpoint_results')) as flow:
        sum(*np.random.randint(1000, size=2))
        sum(*np.random.randint(1000, size=2))
        sum(*np.random.randint(1000, size=2))
        sum(*np.random.randint(1000, size=2))
        sum(*np.random.randint(1000, size=2))

    state = flow.run()
    # Weired thing here, one needs to extract the storage locations from the state object
    # So make sure to persist the state object for later analysis.
    task_result_locations = [state.result[t]._result.location for t in flow.get_tasks()]

    for idx, loc in enumerate(task_result_locations):
        with open(loc, 'rb') as f:
            result = cloudpickle.load(f)
            print(f"Task[{idx}] return: {result}")

if __name__ == '__main__':
    example()