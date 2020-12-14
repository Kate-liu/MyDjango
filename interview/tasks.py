# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from interview import dingtalk


@shared_task
def send_dingtalk_message(message):
    """
    异步发送 钉钉 消息
    :param message:
    :return:
    """
    dingtalk.send(message)
