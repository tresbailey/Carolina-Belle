from __future__ import unicode_literals

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.template import Context
from django.template.loader import get_template
from django.utils.datastructures import SortedDict

from cartridge.shop.templatetags.shop_tags import _order_totals
from mezzanine import template
from mezzanine.conf import settings
from mezzanine.accounts import (get_profile_form, get_profile_user_fieldname,
                                get_profile_for_user, ProfileNotConfigured)
from the_cb.forms import PersonalizationForm
from the_cb.models import Personalization
from the_cb.paypal_views import personalization_pricing


register = template.Library()


@register.inclusion_tag("shop/includes/order_totals.html", takes_context=True)
def my_order_totals(context):
    import pdb
    pdb.set_trace()
    context = _order_totals(context)
    request = context['request']
    personalization_pricing(request, None, request.cart)
    context['personalization_total'] = request.session.get('personalization_total', '0.0')
    context['order_total'] += Decimal(str(context.get('personalization_total', '0.0')))
    return context


@register.simple_tag(takes_context=True)
def personalize_product_form(context, template='includes/personalization_form_fields.html', *args, **kwargs):
    """
    Returns the login form:

    {% login_form as form %}
    {{ form }}

    """
    form = PersonalizationForm(None, *args, **kwargs)
    if kwargs['personalization'] and kwargs['personalization'] is not None:
            form.load(kwargs['personalization'])
    context["form_for_fields"] = form
    return get_template(template).render(Context(context))

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
