from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponse

import logging
import csv
from datetime import datetime

from django.utils.safestring import mark_safe

from interview.models import Candidate
from interview import candidate_fieldset as cf
from interview import dingtalk
from jobs.models import Resume

logger = logging.getLogger(__name__)

exportable_fields = (
    "username", "city", "phone",
    "bachelor_school", "master_school", "degree",
    "first_result", "first_interviewer_user",
    "second_result", "second_interviewer_user",
    "hr_result", "hr_score", "hr_remark", "hr_interviewer_user",
)


# 通知一面面试官
def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers

    # 钉钉发送消息
    dingtalk.send("候选人 %s 进入面试环节，亲爱的面试官，请做好准备: %s" % (candidates, interviewers))
    # 页面提示通知成功信息
    messages.add_message(request, messages.INFO, "已经成功发送面试通知!")


notify_interviewer.short_description = u"通知一面面试官"


# 导出应聘者信息到 csv 文件
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    field_list = exportable_fields
    response["Content-Disposition"] = "attachment; filename=recruitment-candidates-list-%s.csv" % (
        datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for obj in queryset:
        # 单行的记录（各个字段的值），写入到 csv 文件
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    logger.info("%s exported %s candidate record" % (request.user, len(queryset)))

    return response


# 将函数操作的展示变为中文
export_model_as_csv.short_description = u"导出为CSV文件"
# 导出 CSV 文件，需要有 export 权限才可以展示
export_model_as_csv.allowed_permissions = ("export",)


# 候选人，应聘者操作
class CandidateAdmin(admin.ModelAdmin):
    # 排除不展示的字段
    exclude = ("creator", "created_date", "modified_date")

    # 导出信息到csv文件行为
    actions = [export_model_as_csv, notify_interviewer, ]

    # 当前用户是否有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm("%s.%s" % (opts.app_label, "export"))

    # 展示的字段
    list_display = (
        "username", "city", "bachelor_school",
        "get_resume",
        "first_score", "first_result", "first_interviewer_user",
        "second_result", "second_interviewer_user",
        "hr_score", "hr_result",
        "last_editor",
    )

    # 筛选条件
    list_filter = (
        "city",
        "first_result", "second_result", "hr_result",
        "first_interviewer_user", "second_interviewer_user", "hr_interviewer_user",
    )

    # 排序
    ordering = (
        "hr_result", "second_result", "first_result",
    )

    # 查询字段
    search_fields = (
        "username", "phone", "email",
        "bachelor_school",
    )

    # 设置列表编辑面试官，不需要进入详情页，只有 HR 才可以进行设置
    # get_list_editable 不在 Django中，使用get_changelist_instance进行父类方法的覆盖
    default_list_editable = ("first_interviewer_user", "second_interviewer_user",)

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or "hr" in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 设置面试官为只读字段，只有 HR 才可以进行设置
    # readonly_fields = ("first_interviewer_user", "second_interviewer_user",)
    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if "interviewer" in group_names:
            logger.info("interviewer is in user's  group for %s", request.user.username)
            return ("first_interviewer_user", "second_interviewer_user",)
        return ()

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    # 一面面试官仅填写一面反馈，二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        # interviewer 有权限 and 只展示当前登录用户的数据
        if "interviewer" in group_names and obj.first_interviewer_user == request.user:
            return cf.default_field_first
        if "interviewer" in group_names and obj.second_interviewer_user == request.user:
            return cf.default_field_second
        return cf.default_field

    # 对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or "hr" in group_names:
            return qs
        # 使用 Q 表达式做复杂的 and 与 or 查询
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )

    # 列表添加跳转简历详情页列
    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank"> %s </a>' % (resumes[0].id, "查看简历"))
        return ""

    get_resume.short_description = "查看简历"
    get_resume.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


admin.site.register(Candidate, CandidateAdmin)
