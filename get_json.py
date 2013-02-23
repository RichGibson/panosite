from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)

# get_json.py - for every gigapan in Gigapan model get <gigapan_id>.json file.

from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

gigapans = Gigapan.objects.all()
cnt = 0
for g in gigapans:
    filename = "%i.json" % (g.gigapan_id)
    url = "http://gigapan.com/gigapans/%s" % (filename)
    out_file = "json/%s" % filename
    
    # check if filename exists
    try:
       print "check for %s for %s" % ( out_file, g.name ),
       with open(out_file) as f: 
            print "\tfile exists"
            pass
    except IOError as e:
       print "\tfetching %s " % ( url)
       data = urlopen(url).read()

       f = open(out_file,"w")
       f.write(data)
       f.close()
       cnt = cnt+1

