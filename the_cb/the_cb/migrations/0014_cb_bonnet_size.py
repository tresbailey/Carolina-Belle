# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import cartridge.shop.fields


class AddExtraField(migrations.AddField):

    def __init__(self, *args, **kwargs):
        if 'app_label' in kwargs:
            self.app_label = kwargs.pop('app_label')
        else:
            self.app_label = None
        super(AddExtraField, self).__init__(*args, **kwargs)

    def state_forwards(self, app_label, state):
        super(AddExtraField, self).state_forwards(self.app_label or app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        super(AddExtraField, self).database_forwards(
            self.app_label or app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        super(AddExtraField, self).database_backwards(
            self.app_label or app_label, schema_editor, from_state, to_state)


class ChangeExistingField(migrations.AlterField):

    def __init__(self, *args, **kwargs):
        if 'app_label' in kwargs:
            self.app_label = kwargs.pop('app_label')
        else:
            self.app_label = None
        super(ChangeExistingField, self).__init__(*args, **kwargs)

    def state_forwards(self, app_label, state):
        super(ChangeExistingField, self).state_forwards(self.app_label or app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        super(ChangeExistingField, self).database_forwards(
            self.app_label or app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        super(ChangeExistingField, self).database_backwards(
            self.app_label or app_label, schema_editor, from_state, to_state)


class Migration(migrations.Migration):

    dependencies = [
        ('the_cb', '0013_cb_personalization_price'),
    ]

    operations = [
        AddExtraField(
            model_name='productvariation',
            name='option19',
            field=cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Bonnet Size'),
            app_label='shop'
        ),
        ChangeExistingField(
            model_name='productoption',
            name='type',
            field=models.IntegerField(verbose_name='Type', choices=[(1, 'Size'), (2, 'Shoe Size'), (3, 'Gown Color'), (4, 'Thread Color'), (5, 'Font'), (6, 'Monogram Size'), (7, 'Monogram Type'), (8, 'Blanket Type'), (9, 'Pajama Size'), (10, 'Hat Color'), (11, 'Applique Fabric Counts'), (12, 'Boxer Sizes'), (13, 'Linen Bib Fabric'), (14, 'Bloomer Sizes'), (15, 'College Bloomer Teams'), (16, 'Thread Colors'), (17, 'Style'), (18, 'Color'), (19, 'Bonnet Size')]),
            app_label='shop'
        ),
        ChangeExistingField(
            model_name='productvariation',
            name='option1',
            field=cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Size'),
            app_label='shop'
        ),
        ChangeExistingField(
            model_name='productvariation',
            name='option2',
            field=cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Shoe Size'),
            app_label='shop'
        ),
    ]
