# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-28 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20171022_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, upload_to='image/%Y/%m/%d/'),
        ),
    ]