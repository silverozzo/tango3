# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0028_auto_20160329_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmaterialcachedrest',
            name='date',
            field=models.OneToOneField(to='bar.WorkDay'),
        ),
    ]
