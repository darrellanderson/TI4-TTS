#!/usr/bin/python
#
# The Atom/TTS extension supports #include to insert files.  Unfortunately
# when loading scripts from TTS it only adds the #include, so if the user
# does not have the script in question in their filesystem everything breaks.
#
# This quick hack reads a ttslua script, injecting #include content.
# At the time of this writing this is a one-way transformation.

import os
import re
import sys

includePattern = re.compile('^#include <(~/.*)>')
delim = '-- ############################################################################\n'

included = set()

def process(filename, wrapInDoEnd):
    absoluteFilename = os.path.expanduser(filename) + '.ttslua'
    if absoluteFilename in included:
        return
    included.add(absoluteFilename)

    sys.stdout.write(delim)
    sys.stdout.write('-- #### START #include <' + filename + '>\n')
    sys.stdout.write(delim)
    sys.stdout.write('\n')

    if wrapInDoEnd:
        sys.stdout.write('do\n')
        sys.stdout.write('\n')

    insideComment = False
    file = open(absoluteFilename)
    for line in file:

        if line.find('--[[') != -1:
            insideComment = True
        if line.find(']]') != -1:
            insideComment = False
        if line.find('-- #RESET_INCLUDED --'):
            included.clear()

        if line.startswith('#include') and not insideComment:
            m = includePattern.search(line)
            includeFilename = m.group(1)
            process(includeFilename, False)
        else:
            sys.stdout.write(line)

    file.close()

    if wrapInDoEnd:
        sys.stdout.write('\n')
        sys.stdout.write('end\n')

    sys.stdout.write('\n')
    sys.stdout.write(delim)
    sys.stdout.write('-- #### END #include <' + filename + '>\n')
    sys.stdout.write(delim)
    sys.stdout.write('\n')

process(sys.argv[1], False)
sys.stdout.flush()
