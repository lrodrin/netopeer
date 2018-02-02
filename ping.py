"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import os
# !/usr/bin/env python
import sys

x, y, host = sys.argv[4].split()

if (len(sys.argv) == 7):
    count = sys.argv[6]
else:
    count = "1"

str = "ping -c %s %s" % (count, host)
result = os.popen(str).read()

print("""result 'Invoked from %s Ping to %s count %s: %s'""" % (sys.argv[2], host, count, result))
