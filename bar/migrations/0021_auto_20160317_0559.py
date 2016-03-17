# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0020_auto_20160316_0903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saleoffer',
            options={'ordering': ('product__name',)},
        ),
    ]
