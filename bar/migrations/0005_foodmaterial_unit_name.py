# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0004_foodmaterialitem_unit_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodmaterial',
            name='unit_name',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
