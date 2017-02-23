# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import extras.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualInterface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'ordering': ['virtual_machine', 'name'],
            },
        ),
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.CharField(blank=True, help_text='Long-form name (optional)', max_length=100)),
                ('comments', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['group', 'name'],
            },
            bases=(models.Model, extras.models.CustomFieldModel),
        ),
        migrations.CreateModel(
            name='VirtualMachineGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='virtualmachine',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='virtual.VirtualMachineGroup'),
        ),
        migrations.AddField(
            model_name='virtualinterface',
            name='virtual_machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='virtual.VirtualMachine'),
        ),
        migrations.AlterUniqueTogether(
            name='virtualinterface',
            unique_together=set([('virtual_machine', 'name')]),
        ),
    ]