from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)
import os
#tag testing 

from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

tags={}
gigapans = Gigapan.objects.all().filter(owner_id=user_id)
for g in gigapans:
    for tag in g.tags:
        print tag
        #tags{tag}{'num_times'} = tags{tag}{'num_times'}+1	
