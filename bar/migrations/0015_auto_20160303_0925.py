# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0014_recipe_process'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='extra_action',
            field=models.CharField(max_length=250, blank=True),
        ),
    ]
