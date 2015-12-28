# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
        ('the_cb', '001_desire_monogram'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personalization',
            options={},
        ),
        migrations.AlterModelOptions(
            name='personalizationoption',
            options={'verbose_name': 'Personalization option', 'verbose_name_plural': 'Personalization options'},
        ),
        migrations.AlterField(
            model_name='personalization',
            name='value',
            field=models.CharField(max_length=20, null=True, verbose_name='Embroidery Text', blank=True),
        ),
        migrations.AlterField(
            model_name='personalizationoption',
            name='name',
            field=cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='personalizationoption',
            name='type',
            field=models.IntegerField(verbose_name='Type', choices=[(1, 'Embroidery Type'), (2, 'Embroidery Size'), (3, 'Embroidery Thread Color'), (4, 'Embroidery Font')]),
        ),
    ]
