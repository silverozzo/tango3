# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0010_auto_20160303_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleoffer',
            name='cost',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='saleoffer',
            name='price',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=8, decimal_places=2),
        ),
    ]
