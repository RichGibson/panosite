from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)
import os
#check_json - Read the json/*.json files, print out some info

from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

def load_gigapans(dir):
    json_files = os.listdir(dir)
    for file in json_files:
        #print file
        data=json.load(open('json/%s' % file))
        data['gigapan']['gigapan_id'] = data['gigapan']['id']

        # todo: need to understand unicode :-( id  113828 has unicode quotes in it which mess things up.
        print "%i: %s" % (data['gigapan']['gigapan_id'], data['gigapan']['user_id'])
        #print "%i: %s\t%u" % (data['gigapan']['gigapan_id'], data['gigapan']['user_id'], data['gigapan']['name'])
        #print "%i: %s\t" % (data['gigapan']['gigapan_id'], data['gigapan']['user_id']),
        #name = unicode(data['gigapan']['name'])
        #print  unicode(data['gigapan']['name'])

def main():
    load_gigapans('json')

if __name__ == '__main__':
    main()

