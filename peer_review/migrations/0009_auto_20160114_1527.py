# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0008_auto_20151202_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeformItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('freeformType', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='questionLabel',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='label',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='teamdetail',
            name='status',
            field=models.CharField(choices=[('NA', 'Not attempted'), ('IP', 'In progress'), ('C', 'Completed')], default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='userId',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AddField(
            model_name='freeformitem',
            name='question',
            field=models.ForeignKey(to='peer_review.Question'),
        ),
    ]
