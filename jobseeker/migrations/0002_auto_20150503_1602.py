# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('jobseeker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='search_range',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='company',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='education',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.CharField(default=b'', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='job_exp',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='job_type',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='location',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='query_string',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='skills',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
    ]
