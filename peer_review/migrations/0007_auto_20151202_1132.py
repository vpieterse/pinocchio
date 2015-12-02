# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0006_auto_20151202_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamdetail',
            name='status',
            field=models.CharField(choices=[('NA', 'Not attempted'), ('IP', 'In progress'), ('C', 'Completed')], max_length=20, default='Not attempted'),
        ),
        migrations.AlterField(
            model_name='teamdetail',
            name='teamName',
            field=models.CharField(max_length=200, default='emptyTeam'),
        ),
    ]
