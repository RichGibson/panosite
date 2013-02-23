#!/usr/bin/python
# add_tag.py 
# 
# take some parameters, basically add a tag to gigapans which have a certain tag.
# for example, add 'bme' to any gigapan which is bme2007, bme2008, bme2009...etc.
# add roboexotica if roboe2009 exists
# add wien if tag vienna 
#

from django.core.management import setup_environ
from mysite import settings
setup_environ(settings)

from gigapan.models import Gigapan 
from optparse import OptionParser



def main():
  usage = "usage: %prog --oldtag foo --newtag bar"
  description = 'Adds new_tag to gigapans which have the old_tag. does not remove old_tag'
  parser = OptionParser(usage, description=description)
  parser.add_option('-o', '--oldtag', dest='oldtag',
                    help='existing tag')
  parser.add_option('-n', '--newtag', dest='newtag',
                    help='tag to add')
  (options, args) = parser.parse_args()

  #if options.tag and options.match:
  #  parser.error('you may only use --tag or --matching, not both.')
  print "oldtag:%s:" % (options.oldtag)
  #gigapans=Gigapan.objects.all()
  gigapans=Gigapan.objects.filter(tags__name__in=options.oldtag)
  print gigapans
  for g in gigapans:
    print "%i" % (g.id)


  #g.new_from_json(gigapan_data[1])

if __name__ == '__main__':
  main()
