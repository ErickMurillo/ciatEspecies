# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('species', '0003_fctespecies_sci_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fctespecies',
            name='vol_wt_descr_2',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
