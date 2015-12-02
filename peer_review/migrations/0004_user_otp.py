# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0003_questionnaire_questionorders'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='OTP',
            field=models.BooleanField(default=False),
        ),
    ]
