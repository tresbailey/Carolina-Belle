# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cartridge.shop.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20151010_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoption',
            name='type',
            field=models.IntegerField(verbose_name='Type', choices=[(1, "Girl's Size"), (2, "Boy's Size"), (3, 'Gown Color'), (4, 'Thread Color'), (5, 'Font'), (6, 'Monogram Size'), (7, 'Monogram Type'), (8, 'Blanket Type'), (9, 'Pajama Size'), (10, 'Hat Color'), (11, 'Applique Fabric Counts'), (12, 'Boxer Sizes'), (13, 'Linen Bib Fabric'), (14, 'Bloomer Sizes'), (15, 'College Bloomer Teams'), (16, 'Thread Colors'), (17, 'Style'), (18, 'Color')]),
        ),
    ]
