from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt

from jobs.models import Job, Resume
from jobs.models import Cities, JobTypes

import html
import logging

logger = logging.getLogger(__name__)


def joblist(request):
    job_list = Job.objects.order_by("job_type")
    # template = loader.get_template("joblist.html")

    # 上下文
    context = {"job_list": job_list}

    # 将 choices 转为 字符串
    for job in job_list:
        job.type_name = JobTypes[job.job_type][1]
        job.city_name = Cities[job.job_city][1]

    # return HttpResponse(template.render(context))  # 这种方式，在页面上没有 应用上下文，取不到user
    return render(request, "joblist.html", context)


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
        logger.info("job info fetched from database job id: %s" % job_id)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")

    return render(request, 'job.html', {"job": job})


# @csrf_exempt
@permission_required("auth.user_add")
def create_hr_user(request):
    """
    这个URL仅允许有 创建用户权限的用户访问
    """
    if request.method == "GET":
        return render(request, "create_hr.html", {})
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        hr_group = Group.objects.get(name='hr')
        user = User(is_superuser=False, username=username, is_active=True, is_staff=True)
        user.set_password(password)
        user.save()
        user.groups.add(hr_group)

        messages.add_message(request, messages.INFO, "user create %s" % username)
        return render(request, "create_hr.html")
    return render(request, "create_hr.html")


def detail_resume(request, resume_id):
    """
    直接返回 HTML 内容的视图
    （这段代码返回的页面有 XSS 漏洞，能够被攻击者利用）
    """
    try:
        resume = Resume.objects.get(pk=resume_id)
        content = "name: %s <br> introduction: %s <br>" % (resume.username, resume.candidate_introduction)
        # html.escape 进行转义， 不推荐使用
        return HttpResponse(html.escape(content))
    except Resume.DoesNotExist:
        raise Http404("resume does not exist.")


class ResumeDetailView(DetailView):
    """ 简历详情页 """
    model = Resume
    template_name = "resume_detail.html"


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """ 简历职位页面 """
    template_name = "resume_form.html"
    success_url = "/joblist/"
    model = Resume
    fields = [
        "username", "city", "phone",
        "email", "apply_position", "gender",
        "bachelor_school", "master_school", "major", "degree",
        "candidate_introduction", "work_experience", "project_experience",
    ]

    # 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    # 简历跟当前用户关联
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
