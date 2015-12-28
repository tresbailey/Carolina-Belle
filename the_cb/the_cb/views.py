from django.http import JsonResponse
from django.views.generic.edit import CreateView
from mezzanine.utils.views import render, set_cookie, paginate
from the_cb.forms import PersonalizationForm
from the_cb.models import Personalization

def personalization(request, template="personalization.html",
            form_class=PersonalizationForm, extra_context=None):
    model = Personalization
    initial_data = {'type': None, 
        'personal_value': None}
    #if 'POST' == request.method:
    #    import pdb
    #    pdb.set_trace()
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
