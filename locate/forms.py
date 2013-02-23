from django import forms
from django.utils.translation import ugettext as _

from location.utils import parse_location, edit_string_for_location


class LocationWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_location([o.location for o in value.select_related("location")])
        return super(LocationWidget, self).render(name, value, attrs)

class LocationField(forms.CharField):
    widget = LocationWidget

    def clean(self, value):
        value = super(LocationField, self).clean(value)
        try:
            return parse_location(value)
        except ValueError:
            raise forms.ValidationError(_("Please provide a proper location."))
