# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0006_auto_20160222_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmaterialitem',
            name='unit_cost',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
    ]
