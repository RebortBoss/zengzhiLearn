# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-22 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20171030_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', max_length=200, upload_to='teachers/%Y/%m', verbose_name='\u5934\u50cf'),
        ),
    ]