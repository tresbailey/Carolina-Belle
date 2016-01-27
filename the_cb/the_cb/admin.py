from cartridge.shop.admin import ProductAdmin
from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, BaseTranslationModelAdmin
from mezzanine.pages.admin import PageAdmin
from the_cb.models import PersonalizationOption

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

admin.site.register(PersonalizationOption, EmbroideryAdmin)
