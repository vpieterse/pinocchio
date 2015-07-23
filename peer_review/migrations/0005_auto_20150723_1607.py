# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0004_choice_choicetext'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('userId', models.CharField(max_length=8)),
                ('password', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=4)),
                ('initials', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('cell', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=60)),
            ],
        ),
        migrations.RemoveField(
            model_name='studentdetail',
            name='student',
        ),
        migrations.RemoveField(
            model_name='teamdetail',
            name='studentDetail',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='StudentDetail',
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
    ]
