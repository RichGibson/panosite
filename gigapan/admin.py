from gigapan.models import *
from gigapan.models import Issue
from django.contrib import admin

admin.site.register(Gigapan)
#admin.site.register(Issue)
#admin.site.register(InterestingLocation, InterestingLocationAdmin)


#Below the imports, create a new OSMGeoAdmin class, and register the model with the admin package. The OSMGeoAdmin uses OpenStreetMap data for the background, and displays points in a 'spherical mercator' projection.

#class InterestingLocationAdmin(admin.OSMGeoAdmin):
     #list_display = ('name','interestingness')
     #list_filter = ('name','interestingness',)
     #fieldsets = (
       #('Location Attributes', {'fields': (('name','interestingness'))}),
       #('Editable Map View', {'fields': ('geometry',)}),
     #)
 #
    ## Default GeoDjango OpenLayers map options
     #scrollable = False
     #map_width = 700
     #map_height = 325
