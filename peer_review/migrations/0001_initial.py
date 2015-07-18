# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('questionText', models.CharField(max_length=300)),
                ('pubDate', models.DateTimeField(verbose_name='date published')),
                ('questionGrouping', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('intro', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RoundDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('startingDate', models.DateTimeField(verbose_name='starting date')),
                ('endingDate', models.DateTimeField(verbose_name='ending date')),
                ('description', models.CharField(max_length=200)),
                ('questionnaire', models.ForeignKey(to='peer_review.Questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='StudentDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=4)),
                ('initials', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('cell', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=60)),
                ('student', models.ForeignKey(to='peer_review.Student')),
            ],
        ),
        migrations.CreateModel(
            name='TeamDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('teamNumber', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=20)),
                ('roundDetail', models.ForeignKey(to='peer_review.RoundDetail')),
                ('studentDetail', models.ForeignKey(to='peer_review.StudentDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='questionType',
            field=models.ForeignKey(to='peer_review.Type'),
        ),
        migrations.AddField(
            model_name='choice',
            name='header',
            field=models.ForeignKey(to='peer_review.Header'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='peer_review.Question'),
        ),
    ]
