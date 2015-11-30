# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('user_id', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200, null=True, blank=True)),
                ('phone', models.CharField(max_length=200, null=True, blank=True)),
                ('skills', models.CharField(max_length=200, null=True, blank=True)),
                ('education', models.CharField(max_length=200, null=True, blank=True)),
                ('job_exp', models.CharField(max_length=200, null=True, blank=True)),
                ('query_string', models.CharField(max_length=200, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('job_type', models.CharField(max_length=200, null=True, blank=True)),
                ('company', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='HitHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_id', models.CharField(max_length=200)),
                ('hits', models.IntegerField(default=0)),
                ('candidate', models.ForeignKey(to='jobseeker.Candidate')),
            ],
        ),
    ]
