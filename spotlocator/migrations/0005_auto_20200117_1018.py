# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-01-17 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotlocator', '0004_auto_20200115_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menulist',
            name='order_upload',
            field=models.ImageField(blank=True, null=True, upload_to='Order Pics'),
        ),
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='spot logo'),
        ),
    ]
