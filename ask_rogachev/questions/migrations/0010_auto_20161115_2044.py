# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_auto_20161115_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='id',
        ),
        migrations.AlterField(
            model_name='tag',
            name='text',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
