from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from interview.models import DEGREE_TYPE

JobTypes = [
    (0, "技术类"),
    (1, "产品类"),
    (2, "运营类"),
    (3, "设计类")
]

Cities = [
    (0, "北京"),
    (1, "上海"),
    (2, "深圳"),
    (3, "西安")
]


class Job(models.Model):
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name="职位类别")
    job_name = models.CharField(blank=False, max_length=250, verbose_name="职位名称")
    job_city = models.SmallIntegerField(blank=False, choices=Cities, verbose_name="工作地点")
    job_responsibility = models.TextField(max_length=1024, verbose_name="职位职责")
    job_requirement = models.TextField(blank=False, max_length=1024, verbose_name="职位要求")
    # creator = models.CharField(max_length=200, verbose_name="创建人")
    creator = models.ForeignKey(User, verbose_name="创建人", on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    modified_date = models.DateTimeField(verbose_name="修改时间", default=datetime.now)


class Resume(models.Model):
    # Translators: 简历实体的翻译
    username = models.CharField(max_length=135, verbose_name='姓名')
    applicant = models.ForeignKey(User, verbose_name="申请人", null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=135, verbose_name='城市')
    phone = models.CharField(max_length=135, verbose_name='手机号码')
    email = models.EmailField(max_length=135, blank=True, verbose_name='邮箱')
    apply_position = models.CharField(max_length=135, blank=True, verbose_name=u'应聘职位')
    born_address = models.CharField(max_length=135, blank=True, verbose_name=u'生源地')
    gender = models.CharField(max_length=135, blank=True, verbose_name=u'性别')

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=135, blank=True, verbose_name=u'本科学校')
    master_school = models.CharField(max_length=135, blank=True, verbose_name=u'研究生学校')
    doctor_school = models.CharField(max_length=135, blank=True, verbose_name=u'博士生学校')
    major = models.CharField(max_length=135, blank=True, verbose_name='专业')
    degree = models.CharField(max_length=135, choices=DEGREE_TYPE, blank=True, verbose_name=u'学历')
    created_date = models.DateTimeField(verbose_name="创建日期", default=datetime.now)
    modified_date = models.DateTimeField(verbose_name="修改日期", default=datetime.now)

    # 候选人自我介绍，工作经历，项目经历
    candidate_introduction = models.TextField(max_length=1024, blank=True, verbose_name=u'自我介绍')
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name=u'工作经历')
    project_experience = models.TextField(max_length=1024, blank=True, verbose_name=u'项目经历')

    class Meta:
        verbose_name = u'简历'
        verbose_name_plural = u'简历列表'

    def __str__(self):
        return self.username


