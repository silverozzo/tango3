# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0025_auto_20160323_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodMaterialCachedRest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.DecimalField(max_digits=8, decimal_places=4)),
                ('date', models.ForeignKey(to='bar.WorkDay')),
                ('food_material', models.ForeignKey(to='bar.FoodMaterial')),
            ],
            options={
                'ordering': ['-date__date'],
            },
        ),
    ]
