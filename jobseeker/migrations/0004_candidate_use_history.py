# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('jobseeker', '0003_hithistory_hit_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='use_history',
            field=models.BooleanField(default=False),
        ),
    ]
