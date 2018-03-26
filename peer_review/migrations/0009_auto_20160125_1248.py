# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0008_auto_20151202_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='rounddetail',
            name='name',
            field=models.CharField(max_length=15, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='questionLabel',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='label',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='rounddetail',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='rounddetail',
            name='questionnaire',
            field=models.ForeignKey(to='peer_review.Questionnaire', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='userId',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
