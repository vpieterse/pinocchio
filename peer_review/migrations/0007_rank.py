# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0006_auto_20150802_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('firstWord', models.ForeignKey(related_name='RankFirstWord', to='peer_review.Header')),
                ('question', models.ForeignKey(to='peer_review.Question')),
                ('secondWord', models.ForeignKey(related_name='RankSecondWord', to='peer_review.Header')),
            ],
        ),
    ]
