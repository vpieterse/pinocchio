# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peer_review', '0014_remove_freeformitem_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userDetail',
        ),
        migrations.AddField(
            model_name='user',
            name='cell',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='blabla@gmail.com', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='initials',
            field=models.CharField(default='A', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='A', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(default='A', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(default='A', max_length=4),
            preserve_default=False,
        ),
    ]
