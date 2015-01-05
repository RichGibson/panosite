from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)

from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

BASE_URL = 'http://api.gigapan.org/beta'
items = 2000
page=1
per_page=60
#username="rschott"
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
url = "http://api.gigapan.org/beta/gigapans/page/%i/per_page/%i/username/%s/most_recent.json" % (page, per_page, username)

load_gigapans(url)
print "Exit after one page"
#sys.exit(2)
num_pages = items/per_page

# walk the loop, getting and processing more pages
for page in xrange(2,num_pages+1):
    url = "http://api.gigapan.org/beta/gigapans/page/%i/per_page/%i/username/%s/most_recent.json" % (page, per_page, username)
    print "url: %s" %url
    load_gigapans(url)




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


def main():
  usage = "usage: %prog [options] locations.js"
  description = '"load a users gigapans'
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

  if not options.order in ORDER_MAP:
    parser.error('invalid ordering given [popular, recent, size, name]')

  if options.tag and options.match:
    parser.error('you may only use --tag or --matching, not both.')

  create_json(options, args[0])

#if __name__ == '__main__':
#  main()

