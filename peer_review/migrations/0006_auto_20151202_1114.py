# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0005_auto_20151202_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamdetail',
            name='teamNumber',
        ),
        migrations.AddField(
            model_name='teamdetail',
            name='teamName',
            field=models.CharField(max_length=200, default='default'),
            preserve_default=False,
        ),
    ]
