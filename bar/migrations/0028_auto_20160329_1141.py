# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0027_auto_20160329_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmaterialcachedrest',
            name='date',
            field=models.ForeignKey(to='bar.WorkDay', unique=True),
        ),
    ]
