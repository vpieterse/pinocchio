# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0015_auto_20160127_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamdetail',
            name='userDetail',
        ),
        migrations.AddField(
            model_name='teamdetail',
            name='user',
            field=models.ForeignKey(to='peer_review.User', null=True),
        ),
        migrations.DeleteModel(
            name='UserDetail',
        ),
    ]
