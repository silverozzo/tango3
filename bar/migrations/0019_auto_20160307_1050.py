# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0018_accounttransaction_mod_half'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodmaterial',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='foodmaterialitem',
            options={'ordering': ['-when__date']},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='workday',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
