# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0021_auto_20160317_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleoffer',
            name='feasible',
            field=models.BooleanField(default=False),
        ),
    ]
