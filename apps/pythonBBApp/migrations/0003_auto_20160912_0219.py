# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 02:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pythonBBApp', '0002_remove_wishlist_added_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='user_id',
            new_name='user',
        ),
    ]