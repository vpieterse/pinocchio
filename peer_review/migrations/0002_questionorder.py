# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOrder',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('order', models.IntegerField(default=1)),
                ('question', models.ForeignKey(to='peer_review.Question')),
                ('questionnaire', models.ForeignKey(to='peer_review.Questionnaire')),
            ],
        ),
    ]
