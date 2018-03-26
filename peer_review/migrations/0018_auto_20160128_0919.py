# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0017_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
                ('label', models.ForeignKey(to='peer_review.Label')),
                ('question', models.ForeignKey(to='peer_review.Question')),
            ],
        ),
        migrations.AlterField(
            model_name='rounddetail',
            name='name',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='teamdetail',
            name='user',
            field=models.ForeignKey(to='peer_review.User'),
        ),
        migrations.AddField(
            model_name='response',
            name='roundDetail',
            field=models.ForeignKey(to='peer_review.RoundDetail'),
        ),
        migrations.AddField(
            model_name='response',
            name='subjectUser',
            field=models.ForeignKey(related_name='otherUser', to='peer_review.User'),
        ),
        migrations.AddField(
            model_name='response',
            name='user',
            field=models.ForeignKey(related_name='user', to='peer_review.User'),
        ),
    ]
