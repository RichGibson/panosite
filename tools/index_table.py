#!/usr/bin/python

#index_table.py - generate empty tables for regular quadtrees


import math

gigapan_id = 116843
width=100000
height = 100000
levels = 7


def generateTable(level, width, height):
    # at this level and width how many image pixels go into one tile?
    bit = 1 << level >> 1
    width=int(width)
    height=int(height)
    if (bit == 0):
        imageTileWidth  = width
        imageTileHeight = height
    else:
        imageTileWidth  = math.ceil(width / bit)
        imageTileHeight = math.ceil(height / bit)


    if (imageTileWidth > imageTileHeight):
        imageTileSize=imageTileWidth
    else:
        imageTileSize=imageTileHeight

    print "<hr>level: %i width: %i height: %i bit: %i imageTileSize: %i" % (level, width, height, bit, imageTileSize)
    list = []
    print "<table border=\"1\">"

    for row in range(0,math.ceil(height/imageTileSize)):
        print "<tr>"
        for col in range(0,math.ceil(width/imageTileSize)):
            c = [int(col*imageTileSize), int(row*imageTileSize)]
            tilename = getTileFile('',level,c[0],c[1])
            print "<td>",c,"<br>%s</td>" % tilename
            list.append(c)
        print "</tr>"


    print "</table>"
    return list        


def getTileFile(id, level, x, y):
    """Return the filename for the tile which contains the point (x,y) at zoom level 'level'"""
    GC_TILE = ["0", "1", "2", "3"]
    name = "r"
    bit = 1 << level >> 1
    print "getTileFile start level: %i x: %i y: %i\n" % (level, x, y)
    for foo in range(level):
        print "foo: %i" % foo
        if ( (x & bit) > 0) :
            x_index	= 1
        else:
            x_index	= 0
        if ( (y & bit) > 0) :
            y_index	= 2
        else:
            y_index	= 0
        name = name + GC_TILE[( x_index + y_index )]
        #name = name + GC_TILE[( (x and bit) and 1 or 0) + ( (y and bit) and 2 or 0)];
        print "getTileFile %i: x_index %i y_index %i bit: %i name: %s" % (foo, x_index, y_index, bit, name)
        bit = bit >> 1;

    i = 0;
    #while (i < len(name) - 3):
        ## caveat: there is a directory and a file for r00 and r00.jpg and r00123 r00123.jpg
        #url = url + ("/" + name[i:i+3]);
        #i = i + 3;

    return ("%s.jpg"  % (name))


#todo: split getTileName from getTileUrl
#getTileUrl to call getTileName, but getTileName and maybe getTilePath allow for access
#to local tiles
# also, make the directories?
def getTileUrl(id, level, x, y):
    """Return the url for the tile which contains the point (x,y) at zoom level 'level'"""
    url = 'http://share.gigapan.org/gigapans0/%i/tiles' % gigapan_id
    url = 'http://tile%i.gigapan.org/gigapans0/%i/tiles' % (int(gigapan_id/1000), gigapan_id)
    GC_TILE = ["0", "1", "2", "3"]
    name = "r"
    bit = 1 << level >> 1
    for foo in range(level):
        if ( (x & bit) > 0) :
            x_index	= 1
        else:
            x_index	= 0
        if ( (y & bit) > 0) :
            y_index	= 2
        else:
            y_index	= 0
        name = name + GC_TILE[( x_index + y_index )]
        #name = name + GC_TILE[( (x and bit) and 1 or 0) + ( (y and bit) and 2 or 0)];

        bit = bit >> 1;

    i = 0;
    while (i < len(name) - 3):
        # caveat: there is a directory and a file for r00 and r00.jpg and r00123 r00123.jpg
        url = url + ("/" + name[i:i+3]);
        i = i + 3;

    return ("%s/%s.jpg" % (url, name))

def generateTileList(level, width, height):
    # at this level and width how many image pixels go into one tile?
    bit = 1 << level >> 1
    width=int(width)
    height=int(height)
    imageTileWidth  = math.ceil(width / bit)
    imageTileHeight = math.ceil(height / bit)
    if (imageTileWidth > imageTileHeight):
        imageTileSize=imageTileWidth
    else:
        imageTileSize=imageTileHeight

    print "level: %i width: %i height: %i bit: %i imageTileSize: %i" % (level, width, height, bit, imageTileSize)
    list = []
    for row in range(0,math.ceil(height/imageTileSize)):
        for col in range(0,math.ceil(width/imageTileSize)):
            c = [int(col*imageTileSize), int(row*imageTileSize)]
            print c
            list.append(c)
    return list        

# now...get tiles id, level, x, y, height, width?
#print "result of getTileUrl: %s" % getTileUrl(116843,7,9433,1)
#url = getTileUrl(gigapan_id, 1, 0, 0)
#print  "curl -O %s " % url

#TODO: level 3 is not working, the tile names are not counting through the numbers correctly. never 
# getting r001 r011 r111 - the ones place is locked at 0
# level 4 is not really working either.

print """
<pre>
issues
want quadtrees highlighted, each table split in four parts with borders, each of those tables split in 4, etc.
wtf the name is wrong again? 
</pre>
"""
for level in range(1,5):
    generateTable(level, width, height)
