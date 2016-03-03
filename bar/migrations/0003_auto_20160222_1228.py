# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0002_workday_is_current'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.DecimalField(max_digits=8, decimal_places=2)),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('day', models.ForeignKey(to='bar.WorkDay')),
            ],
        ),
        migrations.AddField(
            model_name='foodmaterialitem',
            name='rest',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=4),
        ),
        migrations.AddField(
            model_name='product',
            name='fixed_price',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
        migrations.AddField(
            model_name='saleoffer',
            name='product',
            field=models.ForeignKey(to='bar.Product'),
        ),
    ]
