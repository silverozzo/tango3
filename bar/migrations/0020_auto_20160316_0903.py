# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0019_auto_20160307_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodMaterialSpend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.DecimalField(max_digits=8, decimal_places=4)),
                ('food_material', models.ForeignKey(to='bar.FoodMaterial')),
            ],
        ),
        migrations.AlterModelOptions(
            name='accounttransaction',
            options={'ordering': ('-day',)},
        ),
        migrations.AddField(
            model_name='foodmaterialspend',
            name='transaction',
            field=models.ForeignKey(to='bar.AccountTransaction'),
        ),
        migrations.AddField(
            model_name='foodmaterialspend',
            name='when',
            field=models.ForeignKey(to='bar.WorkDay'),
        ),
    ]
