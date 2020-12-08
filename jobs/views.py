from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from django.http import Http404
from jobs.models import Job
from jobs.models import Cities, JobTypes


def joblist(request):
    job_list = Job.objects.order_by("job_type")
    template = loader.get_template("joblist.html")

    # 上下文
    context = {"job_list": job_list}

    # 将 choices 转为 字符串
    for job in job_list:
        job.type_name = JobTypes[job.job_type][1]
        job.city_name = Cities[job.job_city][1]

    return HttpResponse(template.render(context))


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404("Job does not exist")

    return render(request, 'job.html', {"job": job})
