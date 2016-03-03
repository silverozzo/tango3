# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0005_foodmaterial_unit_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_date', models.DateField()),
                ('what_name', models.CharField(max_length=200)),
                ('what_unit_cost', models.DecimalField(max_digits=8, decimal_places=2)),
                ('what_count', models.DecimalField(max_digits=8, decimal_places=4)),
                ('what_unit_name', models.CharField(max_length=200)),
                ('what_full_cost', models.DecimalField(max_digits=8, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra_action', models.TextField()),
                ('count', models.DecimalField(max_digits=8, decimal_places=4)),
                ('food_material', models.ForeignKey(to='bar.FoodMaterial')),
            ],
        ),
        migrations.RenameModel(
            old_name='Receipt',
            new_name='Recipe',
        ),
        migrations.RemoveField(
            model_name='receiptingredient',
            name='food_material',
        ),
        migrations.RemoveField(
            model_name='receiptingredient',
            name='receipt',
        ),
        migrations.DeleteModel(
            name='ReceiptIngredient',
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(to='bar.Recipe'),
        ),
        migrations.AddField(
            model_name='calculation',
            name='on_prescription',
            field=models.ForeignKey(to='bar.Recipe'),
        ),
    ]
