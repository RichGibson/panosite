from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)
import os
import re
#load_eyegorejson - do something, like load, the json/*.json files from eyegorerihtm

from gigapan.models import Gigapan , Eyegore

import json
import sys
from urllib2 import urlopen

BASE_URL = 'http://api.gigapan.org/beta'
items = 2000
page=1
per_page=60
username="rich"

def load_eye(dir):
    print 'dir: %s' % dir
    json_files = os.listdir(dir)
    for file in json_files:
        if (re.search('\.json$',file)) :
            data=json.load(open('%s/%s' % (dir,file)))
            print file
            m = re.search('^(\d+)',file)
            if m:
                data['gigapan_id'] = m.group(1)
                #print "data: %s"  % data
                print "call Eyegore?" 
                e = Eyegore()
                e.new_from_json(data)

def main():
    load_eye('static/img/eye')

if __name__ == '__main__':
    main()

