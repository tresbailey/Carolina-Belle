from cartridge.shop.admin import ProductAdmin
from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, BaseTranslationModelAdmin
from mezzanine.pages.admin import PageAdmin
from the_cb.models import PersonalizationOption, Personalization

ProductAdmin.fieldsets[0][1]["fields"].extend(["desire_monogram"])
ProductAdmin.fieldsets[0][1]["fields"].extend(["vendor_prohibited"])


class EmbroideryAdmin(BaseTranslationModelAdmin):
    ordering = ("type", "name")
    list_display = ("type", "name")
    list_display_links = ("type",)
    list_editable = ("name",)
    list_filter = ("type",)
    search_fields = ("type", "name")
    radio_fields = {"type": admin.HORIZONTAL}

class PersonalizationAdmin(BaseTranslationModelAdmin):
    ordering = ('value', 'options', 'embroidery_type', 'extra_note')
    list_display = ('value', 'embroidery_type', 'extra_note')
    list_display_links = ('embroidery_type', 'extra_note')
    list_editable = ('value', )
    list_filter = ('embroidery_type', )
    search_fields = ('value', 'options', 'embroidery_type', 'extra_note')

#admin.site.register(PersonalizationOption, EmbroideryAdmin)
admin.site.register(Personalization, PersonalizationAdmin)
