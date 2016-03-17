# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0022_saleoffer_feasible'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='feasible',
            field=models.BooleanField(default=False),
        ),
    ]
