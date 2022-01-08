# Demo the parallel execution of tasks
import time

import prefect
from prefect import task, Flow, Parameter
from prefect import context as prectx
from prefect.executors import DaskExecutor

@task
def sleep(duration):
    # NOTE: one needs to access the context through prefect not having the context importet. When using DASK
    #logger = prectx.get("logger") # Fails
    logger = prefect.context["logger"]
    logger.info(f"Sleeping for {duration} sec")
    time.sleep(duration)


def example():
    duration = Parameter('duration', default=5)
    with Flow('Example 005') as flow:
        sleep(duration)
        sleep(duration)
        sleep(duration)

    # https://docs.prefect.io/orchestration/flow_config/executors.html#daskexecutor
    # Use 4 worker processes, each with 2 threads
    state = flow.run(duration=5, executor=DaskExecutor(
        cluster_kwargs={"n_workers": 4, "threads_per_worker": 2})
    )

if __name__ == '__main__':
    example()