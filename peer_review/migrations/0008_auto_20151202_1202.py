# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0007_auto_20151202_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='questionLabel',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='label',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='questionText',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='intro',
            field=models.CharField(max_length=1000),
        ),
    ]
