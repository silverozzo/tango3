# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0009_auto_20160303_0559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='receipt',
            new_name='recipe',
        ),
        migrations.AddField(
            model_name='calculation',
            name='on_ingredient',
            field=models.ForeignKey(default=None, to='bar.RecipeIngredient'),
        ),
    ]
