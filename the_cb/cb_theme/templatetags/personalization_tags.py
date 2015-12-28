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

