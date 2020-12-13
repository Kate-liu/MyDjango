# -*- coding: utf-8 -*-
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# --settings=settings.local
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

# 务必修改以下值，确保运行时系统安全:
SECRET_KEY = "w$46bks+b3-7f(13#i%v@jwejrnxc$^^#@#@^t@fofizy1^mo9r8(-939243423300"

# 如果仅使用数据库中的账号，以下 LDAP 配置可忽略
# 替换这里的配置为正确的域服务器配置，同时可能需要修改 base.py 中的 LDAP 服务器相关配置:
# 注意：本机只需要启动 openidap 就可以了，每一次查看本机的 Ip, 进行更改
LDAP_AUTH_URL = "ldap://192.168.1.119:389"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "admin_passwd_4_ldap"

INSTALLED_APPS += (
    # other apps for production site
)

# 钉钉群的 WEB_HOOK， 用于发送钉钉消息
# DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxxxx"
DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=bfe2b51e768ea5bf952eea5d2dc39c464797bb46ab104f66b84212535122d993"

# 集成redis缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "mysecret",
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,  # r/w timeout in seconds
        }
    }
}

# 集成 sentry sdk
sentry_sdk.init(
    dsn="http://6bb38054303b4cc38d7c2e2c4e197cee@127.0.0.1:9000/3",
    integrations=[DjangoIntegration()],

    # performance tracing sample rate
    # 采样率，生产环境访问量过大时，建议调小（不用每一个URL请求都记录性能）
    # 所有请求 100% 进行性能采样
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
