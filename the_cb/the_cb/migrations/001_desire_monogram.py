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
        ('shop', '0011_auto_20151010_1429'),
    ]

    operations = [
        AddExtraField(
            model_name='cartitem',
            name='desire_monogram',
            field=models.BooleanField(default=False, help_text='monogram on it', max_length=16, verbose_name='Monogram the product'),
            preserve_default=False,
            app_label='shop'
        ),
        AddExtraField(
            model_name='orderitem',
            name='desire_monogram',
            field=models.BooleanField(default=False, help_text='monogram on it', max_length=16, verbose_name='Monogram the product'),
            preserve_default=False,
            app_label='shop'
        ),
        AddExtraField(
            model_name='product',
            name='desire_monogram',
            field=models.BooleanField(default=False, help_text='monogram on it', max_length=16, verbose_name='Monogram the product'),
            preserve_default=False,
            app_label='shop'
        ),
        migrations.CreateModel(
            name='PersonalizationOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=1, help_text='What will be embroidered', verbose_name='Personalization Type', choices=(
    (1, "Monogram Size"),
    (2, "Thread Color"),
    (3, "Monogram Type")
))),
                ('name', cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Embroidery Value'))
            ]
        ),
        migrations.CreateModel(
            name='Personalization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(help_text='The value to be embroidered', max_length=24)),
                ('options', models.ManyToManyField("PersonalizationOption", blank=True,
                                     verbose_name="Personalization types",
                                     related_name="personalization_selections")),
            ],
            options={
                'verbose_name': 'Personalization',
                'verbose_name_plural': 'Personalizations'
            },
            bases=(models.Model, mezzanine.utils.models.AdminThumbMixin),
        ),
       AddExtraField(
           model_name='cartitem',
           name='personalization',
           field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=False, serialize=False, to='the_cb.Personalization', null=True),
           preserve_default=False,
           app_label='shop'
       ),
       AddExtraField(
           model_name='orderitem',
           name='personalization',
           field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=False, serialize=False, to='the_cb.Personalization', null=True),
           preserve_default=False,
           app_label='shop'
       ),
       AddExtraField(
           model_name='product',
           name='personalization',
           field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=False, serialize=False, to='the_cb.Personalization', null=True),
           preserve_default=False,
           app_label='shop'
       ),
    ]
