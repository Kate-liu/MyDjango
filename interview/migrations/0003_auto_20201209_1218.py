# Generated by Django 3.1.3 on 2020-12-09 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interview', '0002_auto_20201208_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='first_interviewer',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='hr_interviewer',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='second_interviewer',
        ),
        migrations.AddField(
            model_name='candidate',
            name='first_interviewer_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_interviewer_user', to=settings.AUTH_USER_MODEL, verbose_name='面试官'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='hr_interviewer_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hr_interviewer_user', to=settings.AUTH_USER_MODEL, verbose_name='HR面试官'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='second_interviewer_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_interviewer_user', to=settings.AUTH_USER_MODEL, verbose_name='二面面试官'),
        ),
    ]