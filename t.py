#test code - a scratchpad

import shlex
import sys

import shlex
def tagSplit(value):
    # turn a string into a list of tags. Split on space, comma, period, ignore empty strings, 
    # ignore multiple spaces, respect quotes...basically, do the 'right thing' with any random
    # string which looks like tags.
    lex = shlex.shlex(value)
    lex.whitespace +='.,'
    lex.commenters = ''
    return list(lex)

st="tag1,tag2 tag3  tag4, tag5 'tag6 withquotes' tag7"
print st
print "newSplit"
print tagSplit(st)

sys.exit(2)
## this works pretty much
st='string,comma and, spaces  multipespaces, comma space   tag'
a=st.split(None)
tags=[]
for e in a:
  print e
  a2 = e.split(',')
  for e2 in a2:
      tags.append(e2)

print tags
  
