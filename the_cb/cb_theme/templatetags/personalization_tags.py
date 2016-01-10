from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.utils.datastructures import SortedDict

from mezzanine import template
from mezzanine.conf import settings
from mezzanine.accounts import (get_profile_form, get_profile_user_fieldname,
                                get_profile_for_user, ProfileNotConfigured)
from the_cb.forms import PersonalizationForm
from the_cb.models import Personalization


register = template.Library()



@register.as_tag
def personalize_product_form(*args):
    """
    Returns the login form:

    {% login_form as form %}
    {{ form }}

    """
    return PersonalizationForm()


@register.filter
def name_value_options(personalization, option):
    for field in personalization.option_fields():
        if field.name == 'option%s' % option['type']:
            return "%s: %s" % (field.verbose_name, option['name'])
    return None


@register.filter
def embroidery_type_val(personalization_type):
    types = dict(settings.CB_EMBROIDERY_TYPES)
    return types[personalization_type]
