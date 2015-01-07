# Create your views here.

from django.conf import settings
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django import forms
from django.forms import ModelForm

from django.db import connection, transaction

from django.http import HttpResponse
from models import Gigapan, Gallery, User
import os
import re
import math

THUMBNAIL_w = 250
THUMBNAIL_h = 250

def bytag(request, p):
    # make an array of tags, split on space or comma
    #multiple spaces are one space.
    #tags = tagSplit(p)
    tag_list = p.split()
    gigapans=Gigapan.objects.filter(tags__name__in=tag_list)

    if request.method == 'POST':
        form = TagAddForm(request.POST)
        if form.is_valid():
            # process data in  form.cleaned_data
            foo = 'bar'
            # check for lat/long
            # for each gigapan with old tag, check if it has new tag, in theory
            # select * from gigapans where oldtag in (tags) and newtag not in (tags)
    else:
        form = TagAddForm()
        form.latitude = 123
    tags = []
    
    #tags = Gigapan.tags.Filter(tags__name__in=tag_list)

    st = ''
    for g in gigapans:
      # the gigapan.org thumbnail api takes a gigapan id, width, and height and returns 
      # a 'thumbnail' of the image in that size.
      #g.thumbnail_url = "http://api.gigapan.org/beta/gigapans/%i-%ix%i.jpg" % (g.gigapan_id,THUMBNAIL_w,THUMBNAIL_h) 
      g.thumbnail_filename = "%i-800x800.jpg" % (g.gigapan_id) 

    form = TagAddForm()
    return render_to_response('site_master.html', {'gigapans': gigapans, 'page_template': 'gigapans.html', 'form': form, 'p':p, 'tags': tags, 'tag_list':tag_list})

# bytag_edit is broken 
def bytag_edit(request, p):
    # same as by_tag, but with an edit flag

    if request.method == 'POST':
        form = TagAddForm(request.POST)
        if form.is_valid():
            # process data in  form.cleaned_data
            foo = 'bar'
            # check for lat/long
            # for each gigapan with old tag, check if it has new tag, in theory
            # select * from gigapans where oldtag in (tags) and newtag not in (tags)
    else:
        form = TagAddForm()
        form.oldtag = 'testold'
        form.latitude = 123 

    tags = p.split()
    gigapans=Gigapan.objects.filter(tags__name__in=tags)

    st = ''
    for g in gigapans:
      # the gigapan.org thumbnail api takes a gigapan id, width, and height and returns 
      # a 'thumbnail' of the image in that size.
      g.thumbnail_filename = "img/%i-%ix%i.jpg" % (g.gigapan_id,THUMBNAIL_w,THUMBNAIL_h) 

    return render(request, 'index.html', {
        'form': form, 'p':p, 'tme':'foobar'
    })


def calendar(request):
    return calendar_user(request, 0)
    
def calendar_user(request, user_id):
    list = []
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    start_year = 2007
    end_year = 2016
    for year in range(start_year, end_year):
        for month in range(1,13):
            m={}
            m['month'] = month
            m['month_name'] = months[month-1]
            m['year'] = year
            m['cnt'] = 0
            m['gigapan_id'] = 0
            list.append(m)
            i= len(list)-1
    
    from django.db import connection, transaction
    cursor = connection.cursor()
    
    user_clause = '  '
    if user_id > 0:
        user_clause = "and owner_id = %s" % user_id
        
        
    sql = """
            select strftime('%%Y-%%m', uploaded) as d, 
                count(strftime('%%Y-%%m',uploaded)) as cnt ,
                strftime('%%Y',uploaded) as year,
                strftime('%%m',uploaded) as month,
                min(gigapan_id) as gigapan_id_max,
                max(gigapan_id) as gigapan_id_min
            from gigapan_gigapan 
            where month > 0
                and year > 0 
         """
    sql = sql + user_clause + """                 
            group by d order by cnt
            """ #% (user_clause)
    #print "excecute this sql: %s" % sql
    cursor.execute(sql, [])
    #print "after execute"

    desc = cursor.description
    counts = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    # TODO: the end_year constant has to be set or things break.
    for m in counts:
        #print "m %r" % m['cnt']
        #print "year %r" % m['year']
        #print "month %r" % m['month']
        #print "start year %r" % start_year
        #print "end year %r" % end_year
        if (int(m['year']) >= start_year):
            index = (int(m['year']) - start_year) * 12 + int(m['month'])
            #print "index", index
            list[index]['cnt'] = m['cnt'] 
            list[index]['gigapan_id'] = m['gigapan_id_min']
            list[index]['gigapan_id_max'] = m['gigapan_id_max']
            list[index]['gigapan_id_min'] = m['gigapan_id_min']


    return render_to_response('site_master.html', { 'page_template':'calendar.html', 'list': list,})

def docs(request, page):        
    """ My convention is to have a templtes/docs directory. Any files
        dropped into templates/docs magically appear here. Use 
        settings.TEMPLATE_DIRS to decide where to look for docs/ 

        It assumes:
        import os
        from django.conf import settings

        docs.html - a template :-)
 
    """

    docs = [ [d, os.listdir("%s/docs" % d) ] for d in settings.TEMPLATE_DIRS]
    for d in docs:
        d[1].sort()

    # if we have a passed in template page, use it, otherwise default to docs.html
    if len(page) == 0:
        page="docs.html"

    # todo: check that the page exists in the docs list    
    #if  page.rfind('.html') == -1:
    #    page = "%s.html" % page    

    # use the pre tag for txt files
    if re.search(page,'txt'):
        pre=1
    
    return render_to_response('site_master.html', {'pre':1, 'page_template': 'docs/%s' % page, 'sidebar_template':'docs/docs_sidebar.html',     'docs':docs })
#########################################################################
@csrf_exempt
def gigapan(request,id):
    # show one gigapan
    gigapan = Gigapan.objects.get(id=id)
    #gigapan.tagstring = gigapan.tags
    
    if request.method == 'POST':
        form = GigapanEditForm(request.POST, instance=gigapan)
        if form.is_valid():
            # process data in  form.cleaned_data
            form.save()
        else:
            foo = 'foobar'
    else:
        # not a form submission, so populate the form with the current gigapan data
        form = GigapanEditForm(instance=gigapan)
    
    return render_to_response('site_master.html', {'gigapan': gigapan, 'edit':True, 'page_template': 'gigapan.html', 'form': form})


class GigapanEditForm(forms.ModelForm):
    class Meta:
        model = Gigapan

      


def home(request):
    return render_to_response('site_master.html', {'page_template': 'home.html'})






def galleries(request):
    # todo: add gallery pagination
    galleries = Gallery.objects.all()
    start=-1
    end=-1
    page=-1
    return render_to_response('site_master.html', { 'page_template':'galleries.html', 'galleries':galleries,'start':start,'end':end,'page':page, 'prev':page-1, 'next':page+1,})

def gallery(request, id):
    # todo: add gallery pagination
    gallery = Gallery.objects.get(id=id)
    #gigapans = Gigapan.objects.get(galleries=id) 
    st = ''
    start=-1
    end=-1
    page=-1

    #for g in gigapans:
        # the gigapan.org thumbnail api takes a gigapan id, width, and height and returns 
        # a 'thumbnail' of the image in that size.
    #    g.thumbnail_filename = "%i-800x800.jpg" % (g.gigapan_id) 
        #g.thumbnail_url = "http://api.gigapan.org/beta/gigapans/%i-%ix%i.jpg" % (g.gigapan_id,w,h) 
        
    return render_to_response('site_master.html', {'gallery':gallery,'start':start,'end':end, 'gigapans': gigapans,'page':page, 'prev':page-1, 'next':page+1, 'page_template': 'gallery.html'})


def get_location(g):
    # look at a gigapan, g, and return lat, long, and radius based on our best guess determined
    # by the gigapan latitude, longitude, or the highwest resolution tag.
    return (g.latitude,g.longitude,0)

def gfat(request,id):
    # gigapan feature annotation tool
    try:
        gigapan = Gigapan.objects.get(id=id)
    except:
        gigapan = ""
        form = ""
        return render_to_response('site_master.html', {'gigapan': gigapan, 'edit':True, 'page_template': 'gfat.html', 'form': form})

    if request.method == 'POST':
        form = GigapanEditForm(request.POST, instance=gigapan)
        if form.is_valid():
            # process data in  form.cleaned_data
            form.save()
        else:
            foo = 'foobar'
    else:
        # not a form submission, so populate the form with the current gigapan data
        form = GigapanEditForm(instance=gigapan)
    
    return render_to_response('site_master.html', {'gigapan': gigapan, 'edit':True, 'page_template': 'gfat.html', 'form': form})


@csrf_exempt
def gigapan(request,id):
    # show one gigapan
    gigapan = Gigapan.objects.get(id=id)
    user = User.objects.get(owner_id=gigapan.owner_id)
    gigapan.owner_fullname     = "%s %s" % (user.first_name, user.last_name)
    gigapan.first_name     =  user.first_name
    gigapan.last_name     =  user.last_name
    gigapan.username     = user.username
    
    if request.method == 'POST':
        form = GigapanEditForm(request.POST, instance=gigapan)
        if form.is_valid():
            # process data in  form.cleaned_data
            form.save()
        else:
            foo = 'foobar'
    else:
        # not a form submission, so populate the form with the current gigapan data
        form = GigapanEditForm(instance=gigapan)
    
    return render_to_response('site_master.html', {'gigapan': gigapan, 'edit':True, 'page_template': 'gigapan.html', 'form': form})

def gigapans(request, page, user_id):
    return gigapans_parent(request, page, user_id, '')
    
def gigapans_parent(request, page, user_id, format):
    if page == None:
        page=1
    page = int(page)
    
    if re.match('kml',format):
        per_page=999999
    else:    
        per_page=50
    
    start = (page-1)*per_page
    if start < 1:
        start=1
    end = math.ceil(float(page)*per_page)
    if end < 1:
        end = per_page

    end = int(end)

    if user_id > 0:
        gigapans     = Gigapan.objects.all().order_by('-gigapan_id').filter(owner_id=user_id)
        gigapan_cnt = len(gigapans)
        gigapans     = gigapans[start-1:end]
        #gigapans = Gigapan.objects.all().order_by('-gigapan_id').filter(owner_id=user_id)[start:end+1]

        users         = User.objects.all().filter(gigapan_user_id=user_id)
        header        = "Sorted by gigapan id descending for %s %s" % (users[0].first_name, users[0].last_name)
    else:
        gigapans = Gigapan.objects.all().order_by('-gigapan_id')
        #gigapans = Gigapan.objects.all().order_by('aspect')

        gigapan_cnt = len(gigapans)
        #print "gigapan_cnt", gigapan_cnt
        gigapans = gigapans[start-1:end]
        header = 'Sorted by gigapan id descending for all users'
        
    st = ''
    w = 250
    h = 250
    cnt=0
    lat_sum = 0
    lng_sum = 0
    for g in gigapans:
        # the gigapan.org thumbnail api takes a gigapan id, width, and height and returns 
        # a 'thumbnail' of the image in that size.
        g.thumbnail_filename = "%i-800x800.jpg" % (g.gigapan_id) 
        #g.thumbnail_url = "http://api.gigapan.org/beta/gigapans/%i-%ix%i.jpg" % (g.gigapan_id,w,h) 
        #'sidebar_template': 'empty_sidebar.html'
        
        # clean up for KML
        try:
            g.field_of_view_half = float(g.field_of_view_w) / 2 
            pass
        except TypeError as e:
            g.field_of_view_half = 90.0 

        try:
            g.topFov = float(g.field_of_view_h) + float(g.field_of_view_b)
            pass
        except TypeError as e:
            g.topFov = 90.0

        cnt = cnt+1

        try:        
            if ((g.latitude != 0) and (g.longitude != 0)):
                lat_sum = lat_sum + float(g.latitude)
                lng_sum = lng_sum + float(g.longitude)
            pass
        except TypeError as e:
            pass

    # other lookAt values hardcoded for now    
    lookAt = {}
    if cnt > 0:
        lookAt['latitude'] = lat_sum / cnt    
        lookAt['longitude'] = lng_sum / cnt    

    nav = {}
    nav['start']    = start
    nav['end']        = end
    nav['prev']        = page - 0
    nav['page']        = page
    nav['next']        = page + 1
    if user_id > 0:
        nav['next_link'] = "/users/%s/gigapans/%i" % (user_id, nav['next'])
    else:
        nav['next_link'] = "/gigapans/%i" % (nav['next'])
    nav['per_page']    = per_page
    nav['gigapan_cnt']    = gigapan_cnt
    nav['page_cnt']    = int(math.ceil(float(nav['gigapan_cnt']) / per_page))
    
    if re.match('kml',format):
        gigapans = gigapans[1:10]
        return render_to_response('gigapans.kml', {'nav':nav,'lookAt':lookAt,'start':start,'end':end, 'gigapans': gigapans,'page':page, 'prev':page-1, 'next':page+1, 'header':header })        
    else:    
        return render_to_response('site_master.html', {'nav':nav,'lookAt':lookAt,'start':start,'end':end, 'gigapans': gigapans,'page':page, 'prev':page-1, 'next':page+1, 'page_template': 'gigapans.html', 'header':header, 'sidebar_template':'empty_sidebar.html' })



def gigapans_user(request, user_id):
    return gigapans_parent(request, 1, user_id,'')

def gigapans_user_page(request, user_id, page):
    return gigapans_parent(request, page, user_id,'')


def gigapans_kml(request):
    return gigapans_parent(request, 1, 0, 'kml')
    
def gigapans_user_kml(request, user_id):
    return gigapans_parent(request, 1, user_id,'kml')

    
def index(request,page):
    return gigapans(request,page,0)

def index_nopage(request):
    return gigapans(request,1,0)

# TODO: map and mapkml do the same thing, just return a different format. Add a format parameter?
def map(request, p):
    """ return gigapan location to support mapping """
    gigapans = Gigapan.objects.all().order_by('updated')
    for g in gigapans:
      # figure out a location for this gigapan
      (lat,lng,radius) = get_location(g)
      g.thumbnail_url = "/img/%i-800x800.jpg" % (g.gigapan_id) 
      g.thumbnail_url = "http://api.gigapan.org/beta/gigapans/%i-%ix%i.jpg" % (g.gigapan_id,THUMBNAIL_w,THUMBNAIL_h) 

    return render_to_response('map.html', {'gigapans': gigapans, 'p': p})

def mapkml(request, p):
    """ return a kml limited (in theory) to gigapans with georeferencing """
    gigapans = Gigapan.objects.all().order_by('updated')
    st = ''
    for g in gigapans:
      # figure out a location for this gigapan
      (lat,lng,radius) = get_location(g)
      g.thumbnail_url = "/img/%i-800x800.jpg" % (g.gigapan_id) 
      #g.thumbnail_url = "http://api.gigapan.org/beta/gigapans/%i-%ix%i.jpg" % (g.gigapan_id,THUMBNAIL_w,THUMBNAIL_h) 

    return render_to_response('map.kml', {'gigapans': gigapans, 'p': p})


def stats(request):
    return stats_user(request, 0)

def stats_user(request, user_id):
    # do something with statistics...
    # todo: add author filter

    stats = {}
        
    if user_id > 0:
        gigapans=Gigapan.objects.all().order_by("gigapan_id").filter(owner_id=user_id)
        users = User.objects.all().filter(gigapan_user_id=user_id)
        stats['author']=users[0].username
        stats['first_name']=users[0].first_name
        stats['last_name']=users[0].last_name
        stats['owner_id']=user_id

    else:
        gigapans=Gigapan.objects.all().order_by("gigapan_id")
        stats['author']='All users'
        stats['owner_id']=''

    
        
    last_id=0
    last_uploaded = ''
    cnt=0
    stats['gigapan_cnt']=0
    stats['largest_pixels']=0
    stats['total_pixels']=0
    for g in gigapans:
        if last_id == 0:
            last_id = g.gigapan_id
            last_uploaded = g.uploaded
            
        g.last_id = last_id    
        g.gap = g.gigapan_id - last_id
        g.uploaded_gap = g.uploaded - last_uploaded
        cnt=cnt+1
        stats['gigapan_cnt'] = cnt
        pixels = float(g.width*g.height)
        if pixels > stats['largest_pixels']:
            stats['largest_pixels'] = pixels
            stats['largest_id'] = g.id
            stats['largest_gigapan_id'] = g.gigapan_id
            stats['largest_name'] = g.name
        stats['total_pixels'] = stats['total_pixels'] + pixels
        g.cnt = cnt
        last_id = g.gigapan_id
        last_uploaded = g.uploaded

    stats['gigapan_user_id']     = user_id
    stats['largest_pixels']     = stats['largest_pixels']/1e9            
    stats['total_pixels']         = stats['total_pixels']/1e9    
    stats['average_pixels']     = (stats['total_pixels']/stats['gigapan_cnt'])    / 1e9
            
    return render_to_response('site_master.html', {'gigapans': gigapans, 'page_template': 'stats.html', 'stats':stats })




def chart_work(request, user_id):
    # first chart
    # 
    
    stats = {}
        
    if user_id > 0:
        gigapans=Gigapan.objects.all().order_by("gigapan_id").filter(owner_id=user_id) #[0:125]
        users = User.objects.all().filter(gigapan_user_id=user_id)
        stats['author']=users[0].username
        stats['first_name']=users[0].first_name
        stats['last_name']=users[0].last_name
        stats['owner_id']=user_id

    else:
        gigapans=Gigapan.objects.all().order_by("gigapan_id")
        stats['author']='All users'
        stats['owner_id']=''

    
        
    last_id=0
    last_uploaded = ''
    cnt=0
    stats['gigapan_cnt']=0
    stats['largest_pixels']=0
    stats['total_pixels']=0
    for g in gigapans:
        if last_id == 0:
            last_id = g.gigapan_id
            last_uploaded = g.uploaded
            
        g.last_id = last_id    
        g.gap = g.gigapan_id - last_id
        g.uploaded_gap = g.uploaded - last_uploaded
        cnt=cnt+1
        stats['gigapan_cnt'] = cnt
        pixels = float(g.width*g.height)
        if pixels > stats['largest_pixels']:
            stats['largest_pixels'] = pixels
            stats['largest_id'] = g.id
            stats['largest_gigapan_id'] = g.gigapan_id
            stats['largest_name'] = g.name
        stats['total_pixels'] = stats['total_pixels'] + pixels
        g.cnt = cnt
        last_id = g.gigapan_id
        last_uploaded = g.uploaded

    stats['gigapan_user_id']     = user_id
    stats['largest_pixels']     = stats['largest_pixels']/1e9            
    stats['total_pixels']         = stats['total_pixels']/1e9    
    stats['average_pixels']     = (stats['total_pixels']/stats['gigapan_cnt'])    / 1e9
            
    return render_to_response('chartwork.html', {'gigapans': gigapans, 'stats':stats })
    
def chart_user(request, user_id):
    # first chart
    # 
    
    stats = {}
        
    if user_id > 0:
        gigapans=Gigapan.objects.all().order_by("gigapan_id").filter(owner_id=user_id) #[0:125]
        users = User.objects.all().filter(gigapan_user_id=user_id)
        stats['author']=users[0].username
        stats['first_name']=users[0].first_name
        stats['last_name']=users[0].last_name
        stats['owner_id']=user_id

    else:
        gigapans=Gigapan.objects.all().order_by("gigapan_id")
        stats['author']='All users'
        stats['owner_id']=''

    
        
    last_id=0
    last_uploaded = ''
    cnt=0
    stats['gigapan_cnt']=0
    stats['largest_pixels']=0
    stats['total_pixels']=0
    for g in gigapans:
        if last_id == 0:
            last_id = g.gigapan_id
            last_uploaded = g.uploaded
            
        g.last_id = last_id    
        g.gap = g.gigapan_id - last_id
        g.uploaded_gap = g.uploaded - last_uploaded
        cnt=cnt+1
        stats['gigapan_cnt'] = cnt
        pixels = float(g.width*g.height)
        if pixels > stats['largest_pixels']:
            stats['largest_pixels'] = pixels
            stats['largest_id'] = g.id
            stats['largest_gigapan_id'] = g.gigapan_id
            stats['largest_name'] = g.name
        stats['total_pixels'] = stats['total_pixels'] + pixels
        g.cnt = cnt
        last_id = g.gigapan_id
        last_uploaded = g.uploaded

    stats['gigapan_user_id']     = user_id
    stats['largest_pixels']     = stats['largest_pixels']/1e9            
    stats['total_pixels']         = stats['total_pixels']/1e9    
    stats['average_pixels']     = (stats['total_pixels']/stats['gigapan_cnt'])    / 1e9
            
    return render_to_response('chart.html', {'gigapans': gigapans, 'page_template': 'chart.html', 'stats':stats })
    #return render_to_response('site_master.html', {'gigapans': gigapans, 'page_template': 'chart.html', 'stats':stats })


# little form to let us add or edit a form        
class TagAddForm(forms.Form):
    oldtag    = forms.CharField(max_length=100)
    latitude  = forms.FloatField()
    longitude = forms.FloatField()
    newtag    = forms.CharField(max_length=100)


#########################################################################
def tags(request):
    return tags_parent(request, 0,0)
    
def tags_user(request, user_id):
    return tags_parent(request, user_id, 1)

def tag_view(request):
    # no user_id, no page, so pass user_id=0, page=1
    return tags_parent(request, 0, 1)
    
def tags_parent(request, user_id, page):
    max=0
    min=7
    print "tags_parent start"
    page=1
    if page == None:
        page=1
    page = int(page)
    #gigapans = Gigapan.objects.all()
    per_page=24
    start = (page-1)*per_page
    if start < 1:
        start=1
    end = page*per_page
    if end < 1:
        end = per_page

    tags = {}
    if user_id != 0:
        # this does not work
        # tags = Gigapan.tags.most_common().order_by("name").filter(owner_id=user_id)
        
        # this query does what I want, and does it quickly.
        # select tag_id,name, count(tag_id) as cnt 
        # from taggit_taggeditem, taggit_tag 
        # where taggit_taggeditem.tag_id=taggit_tag.id 
        # group by tag_id order by cnt 
        #from django.db import connection, transaction
        cursor = connection.cursor()

        # crap, this doesn't filter by user_id, duh.
        sql = """select tag_id,name, count(tag_id) as num_times, 0 as font_size
                from taggit_taggeditem, taggit_tag 
                where taggit_taggeditem.tag_id=taggit_tag.id 
                group by tag_id 
                order by name """

        sql = """select tag_id,taggit_tag.name, count(tag_id) as num_times , 0 as font_size
            from taggit_taggeditem, taggit_tag , gigapan_gigapan
            where taggit_taggeditem.tag_id=taggit_tag.id 
            and taggit_taggeditem.object_id = gigapan_gigapan.id
            and gigapan_gigapan.owner_id = %s 
            group by tag_id 
            order by taggit_tag.name """ % (user_id)

        sql = """select tag_id,taggit_tag.name, count(tag_id) as num_times , 0 as font_size
            from taggit_taggeditem, taggit_tag , gigapan_gigapan
            where taggit_taggeditem.tag_id=taggit_tag.id 
            and taggit_taggeditem.object_id = gigapan_gigapan.id
            and gigapan_gigapan.owner_id = %s 
            group by tag_id 
            order by count(tag_id) desc """ % (user_id)


        cursor.execute(sql, [])
        desc = cursor.description
        tag_dict = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        # scale font-size from 7-100?
        #tag.num_times = number of occurances
        #first get max occurances
                
        for tag in tag_dict:
            if tag['num_times'] > max:
                max = tag['num_times']
        
        for tag in tag_dict:
            tag['font_size'] = 100.000/max * tag['num_times']
            if tag['font_size'] < 5:
                tag['font_size'] = 0 
            
            # hide tags with view gigapans, then increase the font size for all the tags which survived    
            tag['font_size'] += 5

    else:
        print "tags_parent no user_id, before call to tags.most_common().order_by"
        tags = Gigapan.tags.most_common().order_by("-num_times")
        print "tags_parent no user_id, after call to tags.most_common().order_by"
    
        # scale font-size from 7-100?
        #tag.num_times = number of occurances
        #first get max occurances

        print "tags_parent no user_id before first walk of tags"                
        for tag in tags:
            if tag.num_times > max:
                max = tag.num_times

        print "tags_parent no user_id before second walk of tags"                        
        for tag in tags:
            tag.font_size = 100.000/max * tag.num_times
            if tag.font_size < 9:
                tag.font_size = 0 
            
            # hide tags with view gigapans, then increase the font size for all the tags which survived    
            tag.font_size += 6
        tag_dict = []
        #max = tags[0].num_times
        print "tags_parent no user_id before render to response"                

    return render_to_response('site_master.html', {'max':max, 'start':start,'end':end, 'gigapans': gigapans,'page':page, 'prev':page-1, 'next':page+1, 'page_template': 'tag_view.html', 'tags': tags, 'tag_dict':tag_dict})


   
  
# TODO: better tags
# I want more inclusive tag structure, spaces, commas, quotes, etc. This is code which in theory
# should split a string into tags. But it doesn't work yet.
import shlex
def tagSplit(value):
    # turn a string into a list of tags. Split on space, comma, period, ignore empty strings, 
    # ignore multiple spaces, respect quotes...basically, do the 'right thing' with any random
    # string which looks like tags.
    lex = shlex.shlex(value)
    lex.whitespace +='.,'
    lex.commenters = ''
    return list(lex)

def thumbnail(request,gigapan_id,width,height):
    # return a thumbnail
    # look in thumbnail cache
    # if not found, create gigapan thumbnail url
    # fetch the thumbnail
    # save in local cache
    # return the content
    filename = "%i-%ix%i.jpg" % (gigapan_id,width,height) 
    url = "http://api.gigapan.org/beta/gigapans/%s" % (filename)
    return render_to_response('thumbnail.html', {'filename': filename, 'url': url})

def users(request):
    # To initialize user table
    # insert into gigapan_user values (2,1252,1252,'rschott','Ron','Schott');
    # insert into gigapan_user values (1,353,353,'rich','Rich','Gibson');

    # this won't work because you need the primary key. bah. I probably need a users table
    #sql= "select owner_id, count(owner_id) as cnt from gigapan_gigapan group by owner_id order by owner_id"
    #users = Gigapan.objects.raw(sql) 
    users = User.objects.all().order_by('username')
    return render_to_response('site_master.html', {'users': users, 'page_template': 'users.html',})


