import braintree

from cartridge.shop.checkout import default_tax_handler, default_billship_handler
from cartridge.shop.utils import set_tax, set_shipping
from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView
from mezzanine.conf import settings
from mezzanine.utils.views import render, set_cookie, paginate
from paypal_forms import TokenForm


def cb_billship_handler(request, order_form):
    default_billship_handler(request, order_form)
    set_personalization_cost(request, settings.CB_PERSONALIZATION_COST)

def client_token(request, order_form, template="dropin.html", form_class=TokenForm, extra_content=None):
    if 'clientToken' not in request.session:
        braintree.Configuration.configure(settings.BRAINTREE_ENVIRONMENT,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY)

        token = braintree.ClientToken.generate()
        request.session['clientToken'] = token


def save_nonce(request):
    nonce = request._post['payment_method_nonce']
    request.session['payment_nonce'] = nonce
    return JsonResponse({'nonce': nonce})



def send_payment(request, template="paid.html", form_class=TokenForm, extra_content=None):
    braintree.Configuration.configure(settings.BRAINTREE_ENVIRONMENT,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY)
    nonce = request.session['payment_nonce']
    total_charge = request.cart.total_price() + Decimal(request.session.get('shipping_total', '0.0')) + Decimal(request.session.get('tax_total', '0.0')) + Decimal(str(request.session.get('personalization_total', '0.0')))
    TWOPLACES = Decimal(10) ** -2 
    result = braintree.Transaction.sale({
        "amount": str(total_charge.quantize(TWOPLACES)),
        "payment_method_nonce": nonce
    })
    return result.transaction.id


def set_personalization_cost(request, personalization_total):
    request.session['personalization_total'] = str(personalization_total)


def personalization_pricing(request, order_form, order):
    set_personalization_cost(request, 0)
    personalized_count = sum([item.personalization_price * item.quantity for item in order.items.iterator() if item.personalization and item.personalization.embroidery_type <> 1 and hasattr(item, 'personalization_price')])
    if personalized_count:
        set_personalization_cost(request, personalized_count)
    item_total = sum([item.total_price for item in order.items.iterator()])
    set_tax(request, _("Tax"), (Decimal(request.session.get('personalization_total', '0.0')) + item_total) * Decimal(.06))
    set_shipping(request, _("Flat rate shipping"),
        settings.SHOP_DEFAULT_SHIPPING_VALUE)



