# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-21 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20171016_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='img',
            name='post',
        ),
        migrations.DeleteModel(
            name='Img',
        ),
    ]
