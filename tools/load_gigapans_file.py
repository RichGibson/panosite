from django.core.management import setup_environ
from mysite import settings
setup_environ(settings)

from gigapan.models import Gigapan 

import json
import sys

jsondata=json.load(open('gigapan/my_gigapans.json'))
print jsondata.items

print "loading gigapans"
for gigapan_data in jsondata['items']:
  gigapan_data[1]['gigapan_id'] = gigapan_data[0]
  g = Gigapan()
  g.new_from_json(gigapan_data[1])

