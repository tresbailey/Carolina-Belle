from django.forms.utils import flatatt, to_current_timezone
from django.forms.widgets import Select
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.safestring import mark_safe


class BootstrapSelect(Select):

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs['class'] = 'form-control'
        if self.attrs.get('readonly', False):
            final_attrs['disabled'] = 'disabled'
        output = [format_html('<select{}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))
