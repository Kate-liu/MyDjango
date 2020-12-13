# -*- coding: utf-8 -*-
from celery import Celery

# 第一个参数 是 当前脚本的名称
# 第二个参数 是 broker 的服务地址
# 第三个参数 是 backend 的存储地址
app = Celery('tasks', broker='redis://127.0.0.1', backend="redis://127.0.0.1")


@app.task
def add(x, y):
    return x + y
