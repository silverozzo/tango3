# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0026_foodmaterialcachedrest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='sale_offer',
            field=models.ForeignKey(default=None, blank=True, to='bar.SaleOffer', null=True),
        ),
    ]
