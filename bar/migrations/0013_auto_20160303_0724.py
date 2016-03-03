# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0012_auto_20160303_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmaterial',
            name='unit_name',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
