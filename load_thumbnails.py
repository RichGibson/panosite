from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)


# bad thumbnails can exist...
# to see small ones, which is a characteristic of bad ones
# du -csk *.jpg | sort -n > t
#
# exiftool -T -ImageWidth -ImageHeight -FileName  *.jpg | sort -rn > t
# now t shows images sorted by width, descending.


from gigapan.models import Gigapan 

import json
import sys
from urllib2 import urlopen

username="rich"

width  = 800
height = 800

gigapans = Gigapan.objects.all().order_by('-gigapan_id')
#gigapans = Gigapan.objects.all() #.filter(gigapan_id=38713)
cnt = 0
for g in gigapans:
    filename = "%i-%ix%i.jpg" % (g.gigapan_id,width,height)
    url = "http://api.gigapan.org/beta/gigapans/%s" % (filename)
    out_file = "htdocs/img/%s" % filename
    #out_file = "static/img/%s" % filename
    
    print "%i: (%i, %i)" % (g.gigapan_id, g.width, g.height)
    # check if filename exists
    try:
       print g.name
       print "check for  %s" % ( g.name ),
       with open(out_file) as f: 
        print 
        pass
    except IOError as e:
       print "\tfetching %s" % ( url )
       url = "http://api.gigapan.org/beta/gigapans/%s" % (filename)
       data = urlopen(url).read()

       f = open(out_file,"w")
       f.write(data)
       f.close()
       cnt = cnt+1

    # aspect ratio cleaned up thumbnail
    # calculate an aspect ratio appropriate thumbnail size
    w = float(g.width)
    h = float(g.height)

    print "start: w: %i h: %i" % (w, h)
    ar = h/w
    if w >= h:
        w = 800
        h = height * ar
        print "w >= h w: %i h: %i" % (w, h)
    else:
        h = 800
        w = width * (h/height)
        print "h > w w: %i h: %i" % (w, h)

    filename2 = "%i-%ix%i.jpg" % (g.gigapan_id,w,h)
    url2 = "http://api.gigapan.org/beta/gigapans/%s" % (filename2)
    out_file2 = "htdocs/img/%s.jpg" % (g.gigapan_id) 
    #out_file2 = "static/img/%s.jpg" % (g.gigapan_id) 
    print "filename2: ", filename2
    print "out_file2: ", out_file2
    print url2
    print "ar: %i w: %i h: %i" % (ar, w, h)
    #sys.exit(2)
    try:
       print "check for  %s" % ( out_file2 )
       with open(out_file2) as f: pass
    except IOError as e:
       print "\tfetching %s for  %s" % ( url2, g.name)
        
       url = "http://api.gigapan.org/beta/gigapans/%s" % (filename2)
       data = urlopen(url).read()

       f = open(out_file2,"w")
       f.write(data)
       f.close()
       cnt = cnt+1



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

