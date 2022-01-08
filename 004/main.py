# Demo the usage of Parameters to a flow

from prefect import task, Flow, Parameter
from prefect import context as prectx

@task
def taskA(a, b):
    logger = prectx.get("logger")
    logger.info("Executing task: A")
    return a + b

@task
def taskB(c):
    logger = prectx.get("logger")
    logger.info("Executing task: B")
    logger.info(f"C={c}")


def example():
    a = Parameter("a", default=1)
    b = Parameter("b", default=2)
    with Flow('Example 004') as flow:
        resultA = taskA(a, b)
        taskB(resultA)
    state = flow.run()

    # Rerun flow with different parameters
    state = flow.run(a=10, b=20)

if __name__ == '__main__':
    example()