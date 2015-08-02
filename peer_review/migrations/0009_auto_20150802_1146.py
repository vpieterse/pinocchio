# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0008_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='num',
            field=models.IntegerField(default=1),
        ),
    ]
