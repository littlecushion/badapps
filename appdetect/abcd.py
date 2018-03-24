#!/usr/bin/env python
# encoding: utf-8
import urllib2
import os
f = urllib2.urlopen("http://app.mi.com/download/69155?ref=search") 
filename = os.path.basename(f.url)
with open(filename, "wb") as code:
   code.write(f.read()) 