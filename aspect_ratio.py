
# stats - initiall aspect ratio

from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)

from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen


sum = 0
cnt = 0
gigapans = Gigapan.objects.all()
for g in gigapans:
    g.aspect =  g.width / g.height
    sum = sum + g.aspect
    cnt = cnt + 1
    print g.gigapan_id,g.width,g.height

print "sum: %d cnt: %d " % (sum, cnt)
print 
print (sum/cnt)

