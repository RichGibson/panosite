from django.contrib import admin

from locate.models import Location, LocationItem


class LocationItemInline(admin.StackedInline):
    model = LocationItem

class LocationAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        LocationItemInline
    ]


admin.site.register(Location, LocationAdmin)
