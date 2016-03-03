# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0013_auto_20160303_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='process',
            field=models.TextField(blank=True),
        ),
    ]
