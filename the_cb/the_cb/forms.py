from copy import deepcopy
from decimal import Decimal
from cartridge.shop.forms import AddProductForm
from cartridge.shop.fields import OptionField
from cartridge.shop.models import Cart, Order, SelectedProduct
from django import forms
from django.db.models.fields import Field
from django.forms.models import BaseInlineFormSet, ModelFormMetaclass
from django.forms.models import inlineformset_factory
from django.forms.forms import BoundField
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import smart_text, force_text

from mezzanine.core.forms import Html5Mixin
from the_cb.models import Personalization, PersonalizationOption

class PersonalizationForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Personalization
        fields = ("value",)
    
    def __init__(self, *args, **kwargs):
        super(PersonalizationForm, self).__init__(*args, **kwargs)
        option_fields = Personalization.option_fields()
        option_choices = Personalization.option_choices()
        if not option_fields:
            return
        option_names, option_labels = list(zip(*[(f.name, f.verbose_name)
            for f in option_fields]))
        self.fields['value'] = forms.CharField(label=_('Embroidery Text'))
        for i, name in enumerate(option_fields):
            if name.name in option_choices:
                field = forms.ChoiceField(label=option_labels[i], choices=option_choices[name.name])
                self.fields['%s' % name] = field

    def save(self):
        model = Personalization.objects.create(value=self.data['value'])
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


original_product_add_init = deepcopy(AddProductForm.__init__) 
def product_add_init(self, *args, **kwargs):
    """
    Add student ID to add to cart form
    """
    original_product_add_init(self, *args, **kwargs)
    if self._product:
        self.fields['personalization_id'] = forms.IntegerField()
        self.fields['personalization_id'].widget = forms.HiddenInput()
AddProductForm.__init__ = product_add_init


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
    item, created = self.items.get_or_create(**kwargs)
    if created:
        item.description = force_text(variation)
        item.unit_price = variation.price()
        item.url = variation.product.get_absolute_url()
        try:
            item.personalization_id = variation._personalization_id
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
    import pdb
    pdb.set_trace()
    for item in request.cart:
        product_fields = [f.name for f in SelectedProduct._meta.fields]
        item_dict = dict([(f, getattr(item, f)) for f in product_fields])
        created = self.items.create(**item_dict)
        created.personalization = item.personalization
        created.save()
        
Order.setup = setup
