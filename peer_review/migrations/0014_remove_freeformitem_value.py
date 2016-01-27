# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0013_auto_20160126_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freeformitem',
            name='value',
        ),
    ]
