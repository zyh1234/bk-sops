# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-20 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appmaker', '0007_add_project_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appmaker',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Business', verbose_name='\u6240\u5c5e\u4e1a\u52a1'),
        ),
    ]