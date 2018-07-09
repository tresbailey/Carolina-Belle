# -*- coding: utf-8 -*-
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

       
class Migration(migrations.Migration):

    dependencies = [
        ('the_cb', '0016_vendor_prohib'),
    ]

    operations = [
        AddExtraField(
            model_name='order',
            name='personalization_price',
            field=cartridge.shop.fields.MoneyField(decimal_places=2, default=Decimal('0'), max_digits=10, blank=True, null=True, verbose_name='Personalization price'),
            app_label='shop'
        )
    ]

