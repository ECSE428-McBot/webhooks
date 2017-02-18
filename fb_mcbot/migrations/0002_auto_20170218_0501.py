# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 05:01
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_mcbot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fbuser',
            name='timezone',
        ),
        migrations.AddField(
            model_name='fbuser',
            name='user_id',
            field=models.SlugField(default=b'', max_length=16, validators=[django.core.validators.MinLengthValidator(16)]),
        ),
    ]
