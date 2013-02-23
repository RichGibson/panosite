#!/usr/bin/python

# crop_work.py - work on intelligent cropping

# 1. get an image, likely tiles/r.jpg?
# 2. left margin
left_margin=1
done=0


import Image

img = Image.open('sample.jpg')

w=img.size[0]
h=img.size[1]

# in a column, look at each pixel, if one is not black then move to next row
def left_margin(img):

	for c in range(0:w):
		for r in range(0:h):
			if pixel(c,r) != BLACK|undefined:
				return c 
		if (flag==1):
			#all pixels were black, 		
	return c

def top_margin(img):
	for r in range(0:h):
		for c in range(0:w):
			if pixel(c,r) != BLACK|undefined:
				return r		
	return r

print "python"