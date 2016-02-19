# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FoodMaterialItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.DecimalField(max_digits=8, decimal_places=2)),
                ('count', models.DecimalField(max_digits=8, decimal_places=4)),
                ('food_material', models.ForeignKey(to='bar.FoodMaterial')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptIngredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra_action', models.TextField()),
                ('count', models.DecimalField(max_digits=8, decimal_places=4)),
                ('food_material', models.ForeignKey(to='bar.FoodMaterial')),
                ('receipt', models.ForeignKey(to='bar.Receipt')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='receipt',
            field=models.OneToOneField(to='bar.Receipt'),
        ),
        migrations.AddField(
            model_name='foodmaterialitem',
            name='when',
            field=models.ForeignKey(to='bar.WorkDay'),
        ),
    ]
