# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0007_auto_20160227_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
