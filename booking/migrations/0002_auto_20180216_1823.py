# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-16 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='location',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='booking',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
