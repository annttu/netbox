# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual', '0003_auto_20170222_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualmachinegroup',
            name='description',
            field=models.CharField(blank=True, help_text='Long-form name (optional)', max_length=100),
        ),
    ]