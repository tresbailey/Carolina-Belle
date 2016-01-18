from cartridge.shop.forms import AddProductForm
from cartridge.shop.models import Product, ProductVariation, Order, Cart
from cartridge.shop.views import product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView
from json import dumps
from mezzanine.utils.views import render, set_cookie, paginate
from the_cb.forms import PersonalizationForm
from the_cb.models import Personalization

def personalization(request, template="personalization.html",
            form_class=PersonalizationForm, extra_context=None):
    model = Personalization
    initial_data = {'type': None, 
        'personal_value': None}
    personalize_product = form_class(request.POST or None, initial=initial_data)
    context = {
        'editable_obj': model,
        'personalize_product': personalize_product
    }
    if 'POST' == request.method:
        if personalize_product.is_valid():
           model = personalize_product.save() 
           return JsonResponse({'personalization_id': model.id})
    response = render(request, template, {})
    return response


def cart_item_view(request, template="shop/product.html", form_class=AddProductForm, extra_content=None, cart_id="", item_id=""):
    cart = Cart.objects.filter(id=cart_id).first()
    item = next(item for item in cart.items.iterator() if item.id == int(item_id))
    published_products = Product.objects.published(for_user=request.user)
    product = get_object_or_404(published_products, slug=item.url.split('/')[-1])
    fields = [f.name for f in ProductVariation.option_fields()]
    variations = product.variations.all()
    variations_json = dumps([dict([(f, getattr(v, f))
        for f in fields + ["sku", "image_id"]]) for v in variations])
    variation = ProductVariation.objects.filter(sku=item.sku).first()
    v_json = dict([(f, getattr(variation, f))
        for f in fields + ["sku", "image_id"] if getattr(variation, f) is not None])
    initial_data = dict(quantity=item.quantity, **v_json)
    initial_data['embroidery_type'] = item.personalization.embroidery_type
    initial_data['value'] = item.personalization.value
    
    add_product_form = form_class(request.POST or None, product=product,
                                  initial=initial_data, to_cart=False)
    context = {
        "product": product,
        "editable_obj": product,
        "images": product.images.all(),
        "variations": variations,
        "variations_json": variations_json,
        "has_available_variations": any([v.has_price() for v in variations]),
        "add_product_form": add_product_form,
        "item": item
    }
    return render(request, template, context)
