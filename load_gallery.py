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

def load_gigapans(url):
    #jsondata=json.load(open('gigapan/my_gigapans.json'))
    print "load_gigapans(%s)" % url
    data = urlopen(url)
    print data
    jsondata = json.load(data)
    print jsondata.items

    print "loading gigapans"
    for gigapan_data in jsondata['items']:
      gigapan_data[1]['gigapan_id'] = gigapan_data[0]
      g = Gigapan()
      print "Loading gigapan: %i %s" % (gigapan_data[0], gigapan_data[1]['name'])
      g.new_from_json(gigapan_data[1])
      print "after new from json"

# prime the pump, get the first page
#url = "http://api.gigapan.org/beta/gigapans/page/%i/per_page/%i/username/%s/most_recent.json" % (page, per_page, username)

#load_gigapans(url)
#print "Exit after one page"
#sys.exit(2)
#num_pages = items/per_page

# walk the loop, getting and processing more pages
#for page in xrange(2,num_pages+1):
#    url = "http://api.gigapan.org/beta/gigapans/page/%i/per_page/%i/username/%s/most_recent.json" % (page, per_page, username)
#    print "url: %s" %url
#    load_gigapans(url)




# Helper to build a URL to the API
def create_json(options, out_file):
  url = build_url(options)
  print "INFO: fetching url: %s" % url
  dataio = urlopen(url)
  print "data: %s" % dataio
  data = json.load(dataio)

  locations = []

  if not 'available' in data:
    print "There seems to be a problem with the URL builder. Sorry."
    return
  if data['available'] == 0:
    print "Sorry, no Gigapans match your query."
    return

  items = data['available']
  if options.limit:
    items = min([options.limit, data['available']])
  num_pages = int(ceil(float(items) / data['per_page']))
  for page in xrange(1,num_pages + 1):
    url = build_url(options, page)
    print "INFO: fetching url: %s" % url
    dataio = urlopen(url)
    data = json.load(dataio)

    for (gigapan_id, gigapan) in data['items']:
      if options.user:
        if options.user != gigapan['owner']['username']:
          continue
      if not gigapan['snapshot_set']:
        print "WARNING: Excluding %d: %s as it has no snapshots" % (gigapan_id, gigapan[
'name'])
        continue
      if gigapan['snapshot_set']['count'] == 0:
        print "WARNING: Excluding %d: %s as it has no snapshots" % (gigapan_id, gigapan['name'])
        continue
      snapshot = gigapan['snapshot_set']['items'][0][1]

      loc_line = {
        'id': gigapan_id,
        'height': gigapan['height'],
        'width': gigapan['width'],
        'levels': gigapan['levels'] }
      for k,v in snapshot['bounds'].iteritems():
        loc_line[k] = v
      locations.append(loc_line)

  print "INFO: Writing %s" % out_file
  f = open(out_file, "w")
  f.write("var locations = ")
  json.dump(locations, f, indent=2)
  f.write(";")
  f.close()

def get_gallery_gigapans(line):
	print "\tget_gallery_gigapans: %s" % line
	
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

  load_gallery_from_file(galleryfile)
  #create_json(options, args[0])

if __name__ == '__main__':
  main()

