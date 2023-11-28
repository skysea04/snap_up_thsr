import random

from celery import shared_task

from .celery import app


# @app.task(retry_kwargs={'max_retries': 7, 'countdown': 5})
@app.task()
def add(x, y):
    r = random.randint(0, 1)
    if r:
        raise Exception('aaa')
    # raise Exception('bbb')
    return x + y


# @shared_task
def mul(x, y):
    return x * y


# @shared_task
def xsum(numbers):
    return sum(numbers)
