from prefect import task, Flow
from prefect import context as prectx

@task
def taskA():
    logger = prectx.get("logger")
    logger.info("Executing task: A")

@task
def taskB():
    logger = prectx.get("logger")
    logger.info("Executing task: B")

def example():
    with Flow('Example 000') as flow:
        taskA.set_downstream(taskB)

        flow.run()

if __name__ == '__main__':
    example()