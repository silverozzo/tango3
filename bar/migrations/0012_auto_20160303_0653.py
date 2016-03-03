# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0011_auto_20160303_0629'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='markup',
            field=models.DecimalField(default=1, max_digits=8, decimal_places=2),
        ),
        migrations.AddField(
            model_name='product',
            name='rounding',
            field=models.DecimalField(default=1, max_digits=8, decimal_places=2),
        ),
    ]
