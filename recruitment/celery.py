# -*- coding: utf-8 -*-
import django

django.setup()

# from __future__ import absolute_import, unicode_literals

import os
import json
import time
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
# 保证启动更改文件，而不是使用命令行覆盖，DJANGO_SETTINGS_MODULE=settings.local

app = Celery('recruitment', backend='redis://localhost:6379/1', broker='redis://localhost:6379/0')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# 第一种 定时任务管理
# 需要启动定时任务 beat 才可以加载，然后就开始执行
# 当系统启动之后，执行配置方法，使用一个信号 signal
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='hello every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)


# 第二种 定时任务管理
# 需要启动定时任务 beat 才可以加载，然后就开始执行
# this is important to load the celery tasks
# 显示引入函数，进行执行
from recruitment.tasks import add

app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'recruitment.tasks.add',
        'schedule': 10.0,
        'args': (16, 4,)
    },
}

# 第三种 定时任务管理
# 目前只有这种方式，实现了启动celery的时候，就自动加载了，
# 由于项目是更改配置，自动重新加载，所以一定会 name 重复，报错
# 加载之后不会执行，必须要等到启动beat的时候，才可以执行
# 先创建定时策略
schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)
# 再创建任务
task = PeriodicTask.objects.create(
    interval=schedule,
    # 使用时间戳，保证不会重复，django.core.exceptions.ValidationError: {'name': ['具有 Name 的 Periodic task 已存在。']}
    name="say welcome " + str(time.time()),
    task="recruitment.celery.test",
    args=json.dumps(['welcome rmliu']),
)
