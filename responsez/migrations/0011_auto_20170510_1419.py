# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-10 14:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responsez', '0010_auto_20170510_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalevent',
            name='title',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 10, 14, 19, 15, 939000)),
        ),
    ]
