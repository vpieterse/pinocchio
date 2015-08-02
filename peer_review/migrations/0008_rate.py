# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0007_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numberOfOptions', models.IntegerField(default=5)),
                ('optional', models.BooleanField(default=False)),
                ('num', models.IntegerField(default=0)),
                ('header', models.ForeignKey(to='peer_review.Header')),
            ],
        ),
    ]
