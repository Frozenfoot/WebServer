# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20161210_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='140.jpg', upload_to='avatars/%Y/%m/%d/%H/'),
        ),
    ]