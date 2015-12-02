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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('choiceText', models.CharField(max_length=200)),
                ('num', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('labelText', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('questionText', models.CharField(max_length=300)),
                ('pubDate', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionGrouping',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('grouping', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('intro', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('firstWord', models.CharField(max_length=200)),
                ('secondWord', models.CharField(max_length=200)),
                ('question', models.ForeignKey(to='peer_review.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('numberOfOptions', models.IntegerField(default=5)),
                ('optional', models.BooleanField(default=False)),
                ('num', models.IntegerField(default=0)),
                ('question', models.ForeignKey(to='peer_review.Question')),
            ],
        ),
        migrations.CreateModel(
            name='RoundDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('startingDate', models.DateTimeField(verbose_name='starting date')),
                ('endingDate', models.DateTimeField(verbose_name='ending date')),
                ('description', models.CharField(max_length=200)),
                ('questionnaire', models.ForeignKey(to='peer_review.Questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='TeamDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('teamNumber', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=20)),
                ('roundDetail', models.ForeignKey(to='peer_review.RoundDetail')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('userId', models.CharField(max_length=8)),
                ('password', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=4)),
                ('initials', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('cell', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='userDetail',
            field=models.ForeignKey(to='peer_review.UserDetail'),
        ),
        migrations.AddField(
            model_name='teamdetail',
            name='userDetail',
            field=models.ForeignKey(null=True, to='peer_review.UserDetail'),
        ),
        migrations.AddField(
            model_name='question',
            name='questionGrouping',
            field=models.ForeignKey(to='peer_review.QuestionGrouping'),
        ),
        migrations.AddField(
            model_name='question',
            name='questionType',
            field=models.ForeignKey(to='peer_review.QuestionType'),
        ),
        migrations.AddField(
            model_name='label',
            name='question',
            field=models.ForeignKey(to='peer_review.Question'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='peer_review.Question'),
        ),
    ]
