#!/usr/bin/python

# playing with bit operations

x= 9433
levels=7
bit = 1<<levels<<1
print "x: %i levels: %i bit: %i" % (x, levels, bit)

for i in range(7):
    print "x: %i bit: %i" % (x, bit)
    print x & bit
    bit = bit >> 1

for foo in range(levels):
    print "foo: %i" % foo

