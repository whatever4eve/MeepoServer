# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-10 14:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('responsez', '0008_auto_20170510_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='normalevent',
            name='id',
        ),
        migrations.AddField(
            model_name='normalevent',
            name='baseevent_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='responsez.BaseEvent'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 10, 14, 8, 43, 150000)),
        ),
    ]
