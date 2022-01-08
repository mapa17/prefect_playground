# Demo the parallel execution of tasks
import time

from prefect import task, Flow, Parameter
from prefect import context as prectx

@task
def sleep(duration):
    logger = prectx.get("logger")
    logger.info(f"Sleeping for {duration} sec")
    time.sleep(duration)


def example():
    with Flow('Example 005') as flow:
        
    state = flow.run()

    # Rerun flow with different parameters
    state = flow.run(a=10, b=20)

if __name__ == '__main__':
    example()