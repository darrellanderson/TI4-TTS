#!/usr/bin/python

import re
import sys

testRe = re.compile('^function [\w\.]*\._test\w*\(')

insideTest = False

for line in sys.stdin:
    if insideTest and line.startswith('end'):
        insideTest = False
    elif testRe.match(line):
        insideTest = True
    elif not insideTest:
        sys.stdout.write(line)
