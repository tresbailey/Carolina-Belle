# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('the_cb', '0017_order_personalization_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalization',
            name='extra_note',
            field=models.CharField(max_length=600, null=True, verbose_name='Note to Carolina Belle', blank=True),
        ),
    ]
