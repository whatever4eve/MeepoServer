# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2017-03-24 17:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('responsez', '0003_merge_20170207_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeNof', models.IntegerField(choices=[(0, 'addFriend'), (1, 'message'), (2, 'eventInvite')])),
                ('toUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('userCaused', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsez.UserProfile')),
            ],
        ),
    ]
