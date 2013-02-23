from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)

# load_aspect.py - add aspect ratio, should not be needed later since the model is now set to do that automatically

from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

gigapans = Gigapan.objects.all()
for g in gigapans:
    g.aspect = float(g.width)/g.height
    print "aspect: %f" % g.aspect
    g.save()

