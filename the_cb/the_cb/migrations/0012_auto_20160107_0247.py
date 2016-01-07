from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import mezzanine.utils.models
import mezzanine.core.fields
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
        ('the_cb', '0004_auto_20160107_0220'),
    ]

    operations = [
        AddExtraField(
            model_name='productvariation',
            name='option17',
            field=cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Style'),
            app_label='shop'
        ),
        AddExtraField(
            model_name='productvariation',
            name='option18',
            field=cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Color'),
            app_label='shop'
        ),
        ChangeExistingField(
            model_name='productoption',
            name='type',
            app_label='shop',
            field=models.IntegerField(verbose_name='Type', choices=[(1, "Girl's Size"), (2, "Boy's Size"), (3, 'Gown Color'), (4, 'Thread Color'), (5, 'Font'), (6, 'Monogram Size'), (7, 'Monogram Type'), (8, 'Blanket Type'), (9, 'Pajama Size'), (10, 'Hat Color'), (11, 'Applique Fabric Counts'), (12, 'Boxer Sizes'), (13, 'Linen Bib Fabric'), (14, 'Bloomer Sizes'), (15, 'College Bloomer Teams'), (16, 'Thread Colors'), (17, 'Style'), (18, 'Color')]),
        ),
    ]
