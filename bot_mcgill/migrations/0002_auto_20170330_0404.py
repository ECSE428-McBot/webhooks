# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_mcgill', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mcgillevent',
            name='event_type',
            field=models.CharField(choices=[('event_academic', 'Academic Deadlines'), ('event_facebook', 'Facebook Event'), ('event_misc', 'Misc')], default='event_academic', max_length=70),
        ),
        migrations.AlterField(
            model_name='mcgillevent',
            name='event_link',
            field=models.URLField(blank=True),
        ),
    ]
