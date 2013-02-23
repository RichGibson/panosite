# just play with tag stuff.
from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)

from gigapan.models import Gigapan 

import json
import sys

def one() :
    tags = Gigapan.tags.most_common()
    print  tags
    for tag in tags:
      #gigapan_data[1]['gigapan_id'] = gigapan_data[0]
      #g = Gigapan()
      #g.new_from_json(gigapan_data[1])
      print tag,tag.num_times


def two():
    tags={}
    user_id=353
    gigapans = Gigapan.objects.all().filter(owner_id=user_id)
    for g in gigapans:
        #print "%s: " % (g.gigapan_id),
        t = g.tags.all()
        for tag in t:
            #print "tag:%s:" % tag
            tag = tag.name 
            #print type(tag)
            #tag=string(tag) 
            if tags.get(tag):
                tags[tag] = tags[tag]+1	
            else:
                tags[tag] = 1	
            #tags[tag]['num_times'] = tags[tag]['num_times']+1	
            #tags{tag}{'num_times'} = tags{tag}{'num_times'}+1	
        #print

    for tag in tags:
        print tag, tags[tag]


def three():

    from django.db import connection, transaction
    cursor = connection.cursor()

    # Data modifying operation - commit required
    sql = """select tag_id,name, count(tag_id) as num_times , 0 as font_size
            from taggit_taggeditem, taggit_tag 
            where taggit_taggeditem.tag_id=taggit_tag.id 
            group by tag_id 
            order by name """

    cursor.execute(sql, [])
    desc = cursor.description
    tag_dict = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

    max=0
    min=7

    for tag in tag_dict:
        print tag
        print tag.keys()
        if tag['num_times'] > max:
            max = tag['num_times']
        
    for tag in tag_dict:
        tag['font_size'] = 100.000/max * tag['num_times']
        if tag['font_size'] < 6:
            tag['font_size'] = 0 
            
        # hide tags with view gigapans, then increase the font size for all the tags which survived 
        tag['font_size'] += 5

    for row in tag_dict:
        print row

    print type(tag_dict)
    #r2 = cursor.fetchall()
    #for row in r2:
    #   print row
   
    #row = cursor.fetchone()

def four():

    from django.db import connection, transaction
    cursor = connection.cursor()

    # Data modifying operation - commit required
    sql = """select tag_id,taggit_tag.name, count(tag_id) as num_times , 0 as font_size
            from taggit_taggeditem, taggit_tag , gigapan_gigapan
            where taggit_taggeditem.tag_id=taggit_tag.id 
            and taggit_taggeditem.object_id = gigapan_gigapan.id
            and gigapan_gigapan.owner_id = 1252 
            group by tag_id 
            order by taggit_tag.name """

    cursor.execute(sql, [])
    desc = cursor.description
    tag_dict = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

    max=0
    min=7

    for tag in tag_dict:
        print tag
        print tag.keys()
        if tag['num_times'] > max:
            max = tag['num_times']
        
    for tag in tag_dict:
        tag['font_size'] = 100.000/max * tag['num_times']
        if tag['font_size'] < 6:
            tag['font_size'] = 0 
            
        # hide tags with view gigapans, then increase the font size for all the tags which survived 
        tag['font_size'] += 5

    for row in tag_dict:
        print row

    print type(tag_dict)
    #r2 = cursor.fetchall()
    #for row in r2:
    #   print row
   
    #row = cursor.fetchone()

four()
tags = Gigapan.tags.most_common().order_by("name")
print type(tags)

