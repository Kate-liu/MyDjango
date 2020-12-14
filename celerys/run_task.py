# -*- coding: utf-8 -*-
# https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#id11
from tasks import add

result = add.delay(4, 4)
print("Is task ready: %s" % result.ready())

run_result = result.get(timeout=1)
print("task result: %s" % run_result)
