# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0030_auto_20160329_1212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodmaterialcachedrest',
            options={'ordering': ['-when__date']},
        ),
        migrations.AlterField(
            model_name='foodmaterialcachedrest',
            name='when',
            field=models.ForeignKey(to='bar.WorkDay'),
        ),
    ]
