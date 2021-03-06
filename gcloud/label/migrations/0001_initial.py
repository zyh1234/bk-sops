# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-10 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Label",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=255, verbose_name="标签名称")),
                ("creator", models.CharField(max_length=255, verbose_name="创建者")),
                ("project_id", models.IntegerField(default=-1, verbose_name="项目 ID")),
                ("is_default", models.BooleanField(default=False, verbose_name="默认标签")),
                ("color", models.CharField(default="#dcffe2", max_length=7, verbose_name="标签颜色")),
                ("description", models.CharField(blank=True, max_length=255, null=True, verbose_name="标签描述")),
            ],
            options={"verbose_name": "用户标签 Label", "verbose_name_plural": "用户标签 Label",},
        ),
        migrations.CreateModel(
            name="TemplateLabelRelation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("template_id", models.IntegerField(db_index=True, verbose_name="模版ID")),
                ("label_id", models.IntegerField(db_index=True, verbose_name="标签ID")),
            ],
            options={
                "verbose_name": "模版标签关系 TemplateLabelRelation",
                "verbose_name_plural": "模版标签关系 TemplateLabelRelation",
            },
        ),
        migrations.AlterUniqueTogether(
            name="templatelabelrelation", unique_together=set([("template_id", "label_id")]),
        ),
        migrations.AlterUniqueTogether(name="label", unique_together=set([("project_id", "name")]),),
    ]
