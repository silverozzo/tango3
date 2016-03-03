# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0003_auto_20160222_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodmaterialitem',
            name='unit_cost',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=4),
        ),
    ]
