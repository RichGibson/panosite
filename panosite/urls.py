from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # 
    url(r'^mc', 'mc.views.index'),
    url(r'^mc/docs/(.+)', 'mc.views.docs'),


    #panosite stuff
    url(r'^$', 'gigapan.views.home', name='home'),

    # url(r'^panosite/', include('panosite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^gigapan/(\d+)', 'gigapan.views.gigapan'),

    # gigapan_id (not _our_ id)/width/height
    url(r'^gigapan/thumbnail/(\d+)-(\d+)x(\d+).jpg', 'gigapan.views.thumbnail'),

    url(r'^gigapans/bytag/edit/(.+)$','gigapan.views.bytag_edit'),
    url(r'^gigapans/bytag/(.+)$','gigapan.views.bytag'),
    url(r'^gigapans/gallery/(.+)$','gigapan.views.gallery'),
    url(r'^gigapans/galleries','gigapan.views.galleries'),

    url(r'gigapans/calendar','gigapan.views.calendar'),
    url(r'users/(.+)/calendar','gigapan.views.calendar_user'),
    
    url(r'^gigapans/mapkml(.)?$','gigapan.views.mapkml'),
    url(r'^gigapans/mapkml/(.*)$','gigapan.views.mapkml'),
    url(r'^gigapans/map/(.*)$','gigapan.views.map'),
    url(r'^gigapans/map(.)','gigapan.views.map'),

    url(r'^gigapans/tags','gigapan.views.tags'),
    url(r'^gigapans/tag_view','gigapan.views.tag_view'),
    url(r'^gigapans/stats','gigapan.views.stats'),

    url(r'^gigapans/index/$','gigapan.views.index'),
    url(r'^gigapans/(\d+)?$','gigapan.views.index'),

    url(r'^gigapans.kml','gigapan.views.gigapans_kml'),
    
    url(r'^users/(.+)/gigapans.kml','gigapan.views.gigapans_user_kml'),
    url(r'^users/(.+)/gigapans','gigapan.views.gigapans_user'),
    url(r'^users/(.+)/gigapans','gigapan.views.gigapans_user_page'),

    url(r'^users/(.+)/tags','gigapan.views.tags_user'),
    
    url(r'^users/(.+)/stats','gigapan.views.stats_user'),

    url(r'^users/(.+)/chart_work','gigapan.views.chart_work'),
    url(r'^users/(.+)/chart','gigapan.views.chart_user'),



    url(r'^gigapans/gfat/(\d+)','gigapan.views.gfat'),
    url(r'^gigapans/gfat(.)?','gigapan.views.gfat'),

	# catch all /gigapans link
    url(r'^gigapans','gigapan.views.index_nopage'),

    url(r'^users','gigapan.views.users'),

    
    url(r'^docs/(.*)$','gigapan.views.docs'),

    
    # I really don't understand static urls :-(
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/static/css/'}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/rich/wa/django/panosite/img/'}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/static/js/'}),

)
