from cartridge.shop import views



from copy import deepcopy
from decimal import Decimal
from cartridge.shop.forms import AddProductForm, OrderForm, ADD_PRODUCT_ERRORS
from cartridge.shop.fields import OptionField
from cartridge.shop.models import Cart, Order, SelectedProduct, ProductVariation
from cartridge.shop.utils import recalculate_cart
from django import forms
from django import template
from django.db.models.fields import Field
from django.forms.models import BaseInlineFormSet, ModelFormMetaclass
from django.forms.models import inlineformset_factory
from django.forms.forms import BoundField
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import smart_text, force_text

from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin
from the_cb.models import Personalization, PersonalizationOption
from the_cb.paypal_views import personalization_pricing
from the_cb.widgets import BootstrapSelect


class PersonalizationForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Personalization
        fields = ("value",)
        exclude=['embroidery_type']
    
    def __init__(self, data, personalization=None, template="", *args, **kwargs):
        super(PersonalizationForm, self).__init__(data)
        option_fields = Personalization.option_fields()
        option_choices = Personalization.option_choices()
        if not option_fields:
            return
        option_names, option_labels = list(zip(*[(f.name, f.verbose_name)
            for f in option_fields]))
        self.fields['value'] = forms.CharField(label=_('Value'), widget=forms.HiddenInput())
        for i, name in enumerate(option_fields):
            if name.name in option_choices:
                field = forms.ChoiceField(label=option_labels[i], choices=option_choices[name.name], widget=BootstrapSelect())
                self.fields['%s' % name] = field
        self.fields['embroidery_type'] = forms.IntegerField(widget=forms.HiddenInput())
        self.fields['extra_note'] = forms.CharField(label=_('Note to Carolina Belle'), widget=forms.Textarea(), required=False)

    def save(self):
        model = Personalization.objects.create(value=self.data['value'], embroidery_type=self.data['embroidery_type'], extra_note=self.data['extra_note'])
        prefix = 'the_cb.Personalization.option'
        model.value = self.data['value']
        for field, value in self.data.items():
            if field.startswith(prefix):
                for opt in PersonalizationOption.objects.all():
                    if opt.type == int(field.lstrip(prefix)) and opt.id == int(value):
                        model.options.add(opt)
                        break
        model.save()
        return model

    def load(self, personalization):
        option_fields = Personalization.option_fields()
        option_choices = Personalization.option_choices()
        option_names, option_labels = list(zip(*[(f.name, f.verbose_name)
            for f in option_fields]))
        self.fields['extra_note'].initial = personalization.extra_note
        lookup = dict([('option%s' % opt['type'], opt) for opt in personalization.options.values()])
        for i, name in enumerate(option_fields):
            if name.name in option_choices:
                field = forms.ChoiceField(label=option_labels[i], choices=option_choices[name.name], widget=BootstrapSelect())
                if personalization and personalization is not None:
                    field.initial = lookup.get(name.name, {})['id']
                self.fields['%s' % name] = field
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True


def cb_recalculate_cart(request):
    recalculate_cart(request)
    personalization_pricing(request, None, request.cart)


old_product_view = deepcopy(views.product)
def product_view(request, slug, template="shop/product.html", form_class=AddProductForm, extra_context=None):
    """
    Display a product - convert the product variations to JSON as well as
    handling adding the product to either the cart or the wishlist.
    """
    if extra_context is None:
        extra_context = dict()
    if request.method == 'POST':
        try:
            personalize_product = PersonalizationForm(request.POST)
            if personalize_product.is_valid():
                model = personalize_product.save() 
                copied = request.POST.copy()
                copied['personalization_id'] = model.id
                request.POST = copied
        except AttributeError:
            pass
    extra_context['personalization_cost'] = Decimal(settings.CB_PERSONALIZATION_COST)
    response = old_product_view(request, slug, template, form_class, extra_context)
    cb_recalculate_cart(request)
    return response
views.product = product_view


old_order_view = deepcopy(views.invoice)
def order_view(request, order_id, template="shop/order_invoice.html", template_pdf="shop/order_invoice_pdf.html", extra_context=None):
    order = Order.objects.get_for_user(order_id, request)
    for item in order.items.iterator():
        if item.personalization is not None:
            personalization = Personalization.objects.get_for_user(item.personalization.id, request)
    return old_order_view(request, order_id, template, template_pdf, extra_context)
views.invoice = order_view


original_product_add_init = deepcopy(AddProductForm.__init__) 
def product_add_init(self, *args, **kwargs):
    """
    Add student ID to add to cart form
    """
    original_product_add_init(self, *args, **kwargs)
    self.fields['quantity'] = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    if self._product:
        self.fields['personalization_id'] = forms.IntegerField(required=False)
        self.fields['personalization_id'].widget = forms.HiddenInput()
AddProductForm.__init__ = product_add_init


order_original_init = deepcopy(OrderForm.__init__)
def order_new_init(self, request, step, data=None, initial=None, errors=None):
    self.declared_fields['card_number'].required = False
    self.declared_fields['card_name'].required = False
    self.declared_fields['card_type'].required = False
    self.declared_fields['card_ccv'].required = False
    order_original_init(self, request, step, data, initial, errors)
OrderForm.__init__ = order_new_init


def product_add_clean(self):
    """
    Determine the chosen variation, validate it and assign it as
    an attribute to be used in views.

    """
    if not self.is_valid():
        return
    # Posted data will either be a sku, or product options for
    # a variation.
    data = self.cleaned_data.copy()
    quantity = data.pop("quantity")
    personalization_id = None
    if self._product:
        personalization_id = data.pop("personalization_id")
    # Ensure the product has a price if adding to cart.
    if self._to_cart:
        data["unit_price__isnull"] = False
    error = None
    if self._product is not None:
        # Chosen options will be passed to the product's
        # variations.
        qs = self._product.variations
    else:
        # A product hasn't been given since we have a direct sku.
        qs = ProductVariation.objects
    try:
        variation = qs.get(**data)
    except ProductVariation.DoesNotExist:
        error = "invalid_options"
    else:
        # Validate stock if adding to cart.
        if self._to_cart:
            if not variation.has_stock():
                error = "no_stock"
            elif not variation.has_stock(quantity):
                error = "no_stock_quantity"
    if error is not None:
        raise forms.ValidationError(ADD_PRODUCT_ERRORS[error])
    self.variation = variation
    if personalization_id:
        self.variation._personalization_id = personalization_id
    return self.cleaned_data
AddProductForm.clean = product_add_clean

def add_item_mod(self, variation, quantity):
    """
    Increase quantity of existing item if SKU matches, otherwise create
    new.
    """
    if not self.pk:
        self.save()
    kwargs = {"sku": variation.sku, "unit_price": variation.price()}
    personalized_count = 0
    created = False
    item = self.items.create()
    item.sku = variation.sku
    item.description = force_text(variation)
    item.unit_price = variation.price()
    item.url = variation.product.get_absolute_url()
    try:
        item.personalization_id = variation._personalization_id
        if item.personalization_id is not None and "" <> item.personalization_id:
            item.personalization_price = settings.CB_PERSONALIZATION_COST
            personalized_count += 1
    except AttributeError:
        pass
    image = variation.image
    if image is not None:
        item.image = force_text(image.file)
    variation.product.actions.added_to_cart()
    item.quantity += quantity
    item.save()
Cart.add_item = add_item_mod


def setup(self, request):
    """
    Set order fields that are stored in the session, item_total
    and total based on the given cart, and copy the cart items
    to the order. Called in the final step of the checkout process
    prior to the payment handler being called.

    Also copies personalization IDs
    """
    self.key = request.session.session_key
    self.user_id = request.user.id
    for field in self.session_fields:
        if field in request.session:
            setattr(self, field, request.session[field])
    self.total = self.item_total = request.cart.total_price()
    if self.shipping_total is not None:
        self.shipping_total = Decimal(str(self.shipping_total))
        self.total += self.shipping_total
    if self.discount_total is not None:
        self.total -= Decimal(self.discount_total)
    if self.tax_total is not None:
        self.total += Decimal(self.tax_total)
    self.save()  # We need an ID before we can add related items.
    for item in request.cart:
        product_fields = [f.name for f in SelectedProduct._meta.fields]
        product_fields.append('personalization')
        item_dict = dict([(f, getattr(item, f)) for f in product_fields])
        created = self.items.create(**item_dict)
        created.save()

        
Order.setup = setup


