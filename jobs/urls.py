# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import path
from django.conf import settings

from jobs import views


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    # 职位列表
    url(r"^joblist/", views.joblist, name="joblist"),

    # 职位详情
    url(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),

    # 提交简历
    path("resume/add/", views.ResumeCreateView.as_view(), name="resume-add"),
    path("resume/<int:pk>/", views.ResumeDetailView.as_view(), name="resume-detail"),

    # sentry, creating a route that triggers an error
    path('sentry-debug/', trigger_error),


    path('create_hr_user/', views.create_hr_user, name="create_hr_user"),

    # 首页自动跳转，职位列表
    url(r"^$", views.joblist, name="name"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r"^detail_resume/(?P<resume_id>\d+)/$", views.detail_resume, name="detail_resume"),
    ]
