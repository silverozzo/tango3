# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0029_auto_20160329_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodmaterialcachedrest',
            old_name='date',
            new_name='when',
        ),
    ]
