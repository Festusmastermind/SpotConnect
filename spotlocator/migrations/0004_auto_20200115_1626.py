# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-01-16 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotlocator', '0003_auto_20200115_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menulist',
            name='order_name',
            field=models.CharField(blank=True, choices=[('ch_d', 'Chicken Double Sausage'), ('ch_s', 'Chicken Single Sausage'), ('ch_p', 'Chicken Plain'), ('bf_d', 'Beef Double Sauage'), ('bf_s', 'Beef Single Sauage'), ('bf_p', 'Beef Plain'), ('db_h', 'Double Hotdog')], max_length=5, null=True),
        ),
    ]
