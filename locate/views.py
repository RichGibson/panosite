from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from location.models import LocationItem, Location


def location_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    location = get_object_or_404(Location, slug=slug)
    qs = queryset.filter(pk__in=LocationItem.objects.filter(
        location=location, content_type=ContentType.objects.get_for_model(queryset.model)
    ).values_list("object_id", flat=True))
    if "extra_context" not in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["location"] = location
    return object_list(request, qs, **kwargs)
