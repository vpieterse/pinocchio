# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0003_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='choiceText',
            field=models.CharField(max_length=200, default='Sample choice text'),
            preserve_default=False,
        ),
    ]
