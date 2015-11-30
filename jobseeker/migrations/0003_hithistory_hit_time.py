# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('jobseeker', '0002_auto_20150503_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='hithistory',
            name='hit_time',
            field=models.DateField(default=datetime.datetime(2015, 5, 5, 1, 16, 3, 662993, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
