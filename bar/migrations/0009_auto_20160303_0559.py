# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0008_auto_20160303_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='extra_action',
            field=models.TextField(blank=True),
        ),
    ]
