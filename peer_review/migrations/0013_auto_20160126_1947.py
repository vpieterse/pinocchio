# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0012_auto_20160126_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='num',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='numberOfOptions',
        ),
        migrations.AddField(
            model_name='rate',
            name='bottomWord',
            field=models.CharField(default='peasant', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rate',
            name='topWord',
            field=models.CharField(default='christopher', max_length=25),
            preserve_default=False,
        ),
    ]
