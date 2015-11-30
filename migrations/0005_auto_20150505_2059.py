# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('jobseeker', '0004_candidate_use_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='use_history',
            field=models.CharField(default=b'False', max_length=200, null=True, blank=True),
        ),
    ]
