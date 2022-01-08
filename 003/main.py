# DEMO how to handle 'failing' tasks with automatic retry

import numpy as np

from datetime import timedelta
from prefect import task, Flow
from prefect import context as ptx

@task(max_retries=3, retry_delay=timedelta(seconds=2))
def taskA(a, b):
    # Make use of the context avaiable to all tasks
    logger = ptx["logger"]
    retryCnt = ptx['task_run_count']
    name = ptx["task_full_name"]
    logger.info(f"Running task {name} for the {retryCnt} time ...")

    fail = np.random.choice([False, True], p=[0.8, 0.2])
    if fail:
        logger.info("Made to fail!")
        raise Exception()
    return a + b

def example():
    with Flow('Example 003') as flow:
        r = taskA(1, 2)
        r = taskA(1, 2)
        r = taskA(1, 2)
        r = taskA(1, 2)
        r = taskA(1, 2)
    state = flow.run()

    for idx, result in enumerate([state.result[task_ref].result for task_ref in flow.get_tasks()]):
        print(f"Result of Task {idx} : {result}")

if __name__ == '__main__':
    example()