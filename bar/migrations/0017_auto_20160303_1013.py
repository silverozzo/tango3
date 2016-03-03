# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0016_account_accounttransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='summ',
            field=models.DecimalField(max_digits=8, decimal_places=2, blank=True),
        ),
    ]
