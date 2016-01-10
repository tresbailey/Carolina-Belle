
from __future__ import division, unicode_literals
from collections import defaultdict, OrderedDict
from future.utils import with_metaclass

from cartridge.shop import fields
from django.db import models, connection
from django.db.models import CharField, Manager, Q, F
from django.db.models.base import ModelBase
from django.utils.translation import (ugettext, ugettext_lazy as _,
                                      pgettext_lazy as __)

from mezzanine.conf import settings
from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable, RichText, Orderable, SiteRelated


class PersonalizationMetaclass(ModelBase):
    """
    Metaclass for the ``Personalization`` model that dynamcally
    assigns an ``fields.OptionField`` for each option in the
    ``CB_EMBROIDERY_CHOICES`` setting.
    """
    def __new__(cls, name, bases, attrs):
        # Only assign new attrs if not a proxy model.
        if not ("Meta" in attrs and getattr(attrs["Meta"], "proxy", False)):

            for option in settings.CB_EMBROIDERY_CHOICES:
                attrs["option%s" % option[0]] = fields.OptionField(option[1])
        args = (cls, name, bases, attrs)
        return super(PersonalizationMetaclass, cls).__new__(*args)


class PersonalizationManager(Manager):
    
    def get_for_user(self, personalization_id, request):
        lookup = {"id": personalization_id}
        if not request.user.is_authenticated():
            lookup["key"] = request.session.session_key
        self.get(**lookup)
        


class Personalization(models.Model):
    value = CharField(_("Embroidery Text"), max_length=20, blank=True, null=True)
    options = models.ManyToManyField("PersonalizationOption", blank=True,
                                     verbose_name=_("Personalization types"),
                                     related_name="personalization_selections")
    embroidery_type = models.IntegerField(choices=settings.CB_EMBROIDERY_TYPES)

    objects = PersonalizationManager()

    @classmethod
    def option_fields(cls):
        """
        Returns each of the model files created from CB_EMBROIDERY_CHOICES
        """
        templ = 'option%s'
        attrs = tuple(fields.OptionField(option[1], name=templ % option[0]) for option in settings.CB_EMBROIDERY_CHOICES)
        for opt in attrs:
            opt.model = cls
        return cls._meta.fields + attrs

    @classmethod
    def option_choices(cls):
        options = defaultdict(list)
        for option in PersonalizationOption.objects.all():
            options['option%s' % option.type].append((option.id, option.name))
        return options
    
   
    def filters(self):
        """
        Returns product filters as a Q object for the category.
        """
        # Build a list of Q s to filter variations by.
        filters = []
        # Build a lookup dict of selected options for variations.
        options = self.options.as_fields()
        if options:
            lookup = dict([("%s__in" % k, v) for k, v in options.items()])
            filters.append(Q(**lookup))
        # Q objects used against variations to ensure sale date is
        # valid when filtering by sale, or sale price.
        n = now()
        # Turn the variation filters into a product filter.
        operator = iand if self.combined else ior
        if filters:
            filters = reduce(operator, filters)
            variations = PersonalizationOptions.objects.filter(filters)
            filters = [Q(variations__in=variations)]
            # If filters exist, checking that products have been
            # selected is neccessary as combining the variations
            # with an empty ID list lookup and ``AND`` will always
            # result in an empty result.
            return reduce(operator, filters)
        return None
    

class PersonalizationOptionManager(Manager):
    def as_fields(self):
        options = defaultdict(list)
        for option in self.all():
            options['option%s' % option.type].append(option.name)
        return options
    

class PersonalizationOption(models.Model):
    """
    A selectable option for a personalization such as thread color or size
    """
    type = models.IntegerField(_("Type"),
                               choices=settings.CB_EMBROIDERY_CHOICES)
    name = fields.OptionField(_("Name"))

    objects = PersonalizationOptionManager()

    def __str__(self):
        return "%s: %s" % (self.get_type_display(), self.name)

    def match_option(self, option_name):
        for obj in self.objects.all():
            if obj.type == option_name.lstrip('option'):
                return obj
        return None

    class Meta:
        verbose_name = _("Personalization option")
        verbose_name_plural = _("Personalization options")
