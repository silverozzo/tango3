# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0017_auto_20160303_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttransaction',
            name='mod_half',
            field=models.BooleanField(default=False),
        ),
    ]
