# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_mcbot', '0003_auto_20170331_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='types',
            field=models.ManyToManyField(to='fb_mcbot.EventType'),
        ),
    ]
