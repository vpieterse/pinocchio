# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0002_questionorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='questionOrders',
            field=models.ManyToManyField(through='peer_review.QuestionOrder', to='peer_review.Question'),
        ),
    ]
