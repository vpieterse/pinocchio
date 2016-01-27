# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0016_auto_20160127_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=datetime.datetime(2016, 1, 27, 9, 19, 26, 79255, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
