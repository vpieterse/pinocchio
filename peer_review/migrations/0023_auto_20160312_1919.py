# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0022_auto_20160203_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='label',
            field=models.ForeignKey(null=True, to='peer_review.Label'),
        ),
        migrations.AlterField(
            model_name='response',
            name='subjectUser',
            field=models.ForeignKey(null=True, related_name='otherUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
