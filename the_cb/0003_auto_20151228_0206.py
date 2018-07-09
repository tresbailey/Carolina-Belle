# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20151228_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='personalization',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='personalization',
        ),
        migrations.RemoveField(
            model_name='product',
            name='personalization',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='desire_monogram',
            field=models.BooleanField(default=False, help_text='monogram on it', max_length=16, verbose_name='Monogram the product'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='desire_monogram',
            field=models.BooleanField(default=False, help_text='monogram on it', max_length=16, verbose_name='Monogram the product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='desire_monogram',
            field=models.BooleanField(default=False, help_text='monogram on it', max_length=16, verbose_name='Monogram the product'),
        ),
    ]
