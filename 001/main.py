# Demo Basic task execution

from prefect import task, Flow
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
    with Flow('Example 001') as flow:
        resultA = taskA(1, 2)
        print(f"During task definition: resultA={resultA}")
        taskB(resultA)
    state = flow.run()

    task_ref = flow.get_tasks()[0]
    realized_resultA = state.result[task_ref].result
    print(f"Result of Task A: {realized_resultA}")

if __name__ == '__main__':
    example()