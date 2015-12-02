# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0004_user_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='OTP',
            field=models.BooleanField(default=True),
        ),
    ]
