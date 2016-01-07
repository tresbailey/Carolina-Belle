# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('the_cb', '003_embroidery_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalizationoption',
            name='type',
            field=models.IntegerField(verbose_name='Type', choices=[(2, 'Size'), (3, 'Thread Color'), (4, 'Font')]),
        ),
    ]
