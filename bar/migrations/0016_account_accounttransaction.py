# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0015_auto_20160303_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('is_default', models.BooleanField(default=False)),
                ('costed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AccountTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summ', models.DecimalField(max_digits=8, decimal_places=2)),
                ('account', models.ForeignKey(to='bar.Account')),
                ('day', models.ForeignKey(to='bar.WorkDay')),
                ('sale_offer', models.ForeignKey(to='bar.SaleOffer')),
            ],
        ),
    ]
