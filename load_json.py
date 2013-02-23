from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)
import os
#load_json - load json/*.json files into the gigapan_gigapan model

from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

BASE_URL = 'http://api.gigapan.org/beta'
items = 2000
page=1
per_page=60
username="rich"

def load_gigapans(dir):
    json_files = os.listdir(dir)
    for file in json_files:
        print file
        data=json.load(open('json/%s' % file))
        data['gigapan']['gigapan_id'] = data['gigapan']['id']
        g = Gigapan()
        g.new_from_new_json(data['gigapan'])

def main():
    load_gigapans('json')

if __name__ == '__main__':
    main()

