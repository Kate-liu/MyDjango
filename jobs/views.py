from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from jobs.models import Job, Resume
from jobs.models import Cities, JobTypes


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
    except Job.DoesNotExist:
        raise Http404("Job does not exist")

    return render(request, 'job.html', {"job": job})


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

