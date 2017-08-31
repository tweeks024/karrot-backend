# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 13:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0020_auto_20170831_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='given_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to=settings.AUTH_USER_MODEL),
        ),
    ]