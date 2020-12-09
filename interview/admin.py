from django.contrib import admin
from django.http import HttpResponse

import logging
import csv
from datetime import datetime

from interview.models import Candidate

logger = logging.getLogger(__name__)

exportable_fields = (
    "username", "city", "phone",
    "bachelor_school", "master_school", "degree",
    "first_result", "first_interviewer_user",
    "second_result", "second_interviewer_user",
    "hr_result", "hr_score", "hr_remark", "hr_interviewer_user",
)


# 导出应聘者信息到 csv 文件
def export_model_as_csv(modeadmin, request, queryset):
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


class CandidateAdmin(admin.ModelAdmin):
    # 排除不展示的字段
    exclude = ("creator", "created_date", "modified_date")

    # 导出信息到csv文件行为
    actions = [export_model_as_csv, ]

    # 展示的字段
    list_display = (
        "username", "city", "bachelor_school",
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

    # 字段集合，分块展示
    fieldsets = (
        (None, {"fields": (
            "userid",
            ("username", "city", "phone"),
            ("email", "apply_position", "born_address"),
            ("gender", "candidate_remark", "bachelor_school"),
            ("master_school", "doctor_school"),
            ("major", "degree"),
            ("test_score_of_general_ability", "paper_score"),
            "last_editor",
        )}),
        ("第一轮面试", {"fields": (
            "first_score",
            ("first_learning_ability", "first_professional_competency"),
            "first_advantage", "first_disadvantage", "first_result",
            "first_recommend_position", "first_interviewer_user", "first_remark",)}),
        ("第二轮面试(专业复试)", {"fields": (
            "second_score",
            ("second_learning_ability", "second_professional_competency"),
            ("second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"),
            "second_advantage", "second_disadvantage", "second_result", "second_recommend_position",
            "second_interviewer_user", "second_remark",)}),
        ("HR复试记录", {"fields": (
            "hr_score",
            ("hr_responsibility", "hr_communication_ability"),
            ("hr_potential", "hr_stability"),
            "hr_advantage", "hr_disadvantage",
            "hr_result", "hr_interviewer_user", "hr_remark",)}),
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

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


admin.site.register(Candidate, CandidateAdmin)
