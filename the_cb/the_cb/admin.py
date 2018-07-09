from cartridge.shop.admin import ProductAdmin, OrderAdmin
from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, BaseTranslationModelAdmin
from mezzanine.pages.admin import PageAdmin
from the_cb.models import PersonalizationOption, Personalization

ProductAdmin.fieldsets[0][1]["fields"].extend(["desire_monogram"])
ProductAdmin.fieldsets[0][1]["fields"].extend(["vendor_prohibited"])
OrderAdmin.fieldsets[2][1]["fields"] = OrderAdmin.fieldsets[2][1]["fields"] + ("personalization_pricing",)


class PersonalizationAdmin(BaseTranslationModelAdmin):
    ordering = ('value', 'options', 'embroidery_type', 'extra_note')
    list_display = ('value', 'embroidery_type', 'extra_note')
    list_display_links = ('embroidery_type', 'extra_note')
    list_editable = ('value', )
    list_filter = ('embroidery_type', )
    search_fields = ('value', 'options', 'embroidery_type', 'extra_note')

admin.site.register(Personalization, PersonalizationAdmin)
