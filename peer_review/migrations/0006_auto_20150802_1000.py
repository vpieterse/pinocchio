# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0005_auto_20150723_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionGrouping',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('grouping', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='questionGrouping',
            field=models.ForeignKey(to='peer_review.QuestionGrouping'),
        ),
    ]
