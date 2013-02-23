from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)
from optparse import OptionParser

import re
#import gigapan.models
from gigapan.models import Gigapan, Gallery
#from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

items = 2000
page=1
per_page=60
username="rich"

def get_gallery_gigapans(galleryfile):
    print "\tget_gallery_gigapans: %s" % galleryfile
    f = open(galleryfile, "r")
    lines = f.readlines()
    list = {}
    for line in lines:
        m=re.search("/galleries/(\d+)/gigapans/(\d+)", line)
        if m:
            gallery_id = m.group(1)
            gigapan_id = int(m.group(2))
            list[gigapan_id] = gallery_id

    # now walk the list, download the .json files
    for g in list:
        url = "http://gigapan.com/gigapans/%s.json" % g
        outfile = "%s.json" % g
        try:
            with open("json/%s" % outfile) as f: pass
            print "%s exists" % outfile 
        except IOError as e:
            print "fetching %s" % (outfile)
            data=urlopen(url).read()
            
            f = open(outfile,"w")
            f.write(data)
            f.close()


	
def load_gallery_from_file(galleryfile):
	f = open(galleryfile, "r")
	lines = f.readlines()
	for line in lines:
		m=re.search("galleries/(\d+)/gigapans\">(.+)</a>", line)
		if m:
			name = m.group(2)
			gallery_id = int(m.group(1))
			description = ''
			owner = 'rschott'
			g = Gallery()
			gallery_data = {'gallery_id': gallery_id, 'name': name, 'description':description, 'owner':owner}

      		print "Loading gallery: %i %s" % (gallery_id, name)
      		g.new_from_json(gallery_data)
      		
      		get_gallery_gigapans(line)
	
def main():
  usage = "usage: %prog [options] listfile"
  description = '"load galleries from a file'
  parser = OptionParser(usage, description=description)
  parser.add_option('-t', '--tag', dest='tag',
                    help='find gigapans with a certain tag')
  parser.add_option('-m', '--matching', dest='match',
                    help='find gigapnas matching the given phrase')
  parser.add_option('-u', '--user', dest='user',
                    help='find gigapans belonging to the given username')
  parser.add_option('-o', '--order', dest='order',
                    default='name',
                    help='order gigapans [popular, recent, size, name]')
  parser.add_option('-l', '--limit', dest='limit', type='int',
                    help='limit the number of results to the given limit')
  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.error('must provide a destination file')

  galleryfile = args[0]
  print "load from file: %s" % galleryfile

  get_gallery_gigapans(galleryfile)
  #create_json(options, args[0])

if __name__ == '__main__':
  main()

