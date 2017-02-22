# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenancy', '0003_auto_20170222_1210'),
        ('virtual', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='virtualmachine',
            options={'ordering': ['group', 'name', 'tenant']},
        ),
        migrations.AddField(
            model_name='virtualmachine',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='virtual_machines', to='tenancy.Tenant'),
        ),
    ]
