# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0009_auto_20160114_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userDetail',
            field=models.OneToOneField(to='peer_review.UserDetail'),
        ),
    ]
