#!/usr/bin/python
# Read "copy/paste" mostly-good text from LRR PDF, attempt to distill contents.

import re
import sys

reSection = re.compile('^[0-9]+$')
rePageNumber = re.compile('^[0-9]+$')
reIndex = re.compile('[0-9]+\.[0-9]+$')
reSubsection = re.compile('^[0-9]+\.[0-9]+$')
reAllCaps = re.compile('^[A-Z][A-Z ]+$')

pageNumber = False
lines = [['']]

# Parse into sections, subsections.
for line in sys.stdin:
    # Skip table of contents entries.
    if '. . . .' in line:
        continue

    # Line numbers are a line with only a number.
    if rePageNumber.search(line):
        pageNumber = int(line)
        continue
    if reIndex.search(line):
        continue

    if pageNumber in [38, 39]:
        continue

    if reAllCaps.match(line):
        lines.append([ '***TITLE***' ])

    if line.startswith('Q: '):
        lines.append([ '***QA***' ])

    for term in line.split():
        # Subsection header (not always at start of line)
        if reSubsection.search(term):
            if lines[-1][-1] != '.':
                lines.append([ '***SUBSECTION***' ])

        # Take more care with section headers.  If an all caps term
        # check if previous was a section header, split to new line.
        if reAllCaps.search(term):
            if reSection.search(lines[-1][-1]):
                prevTerm = lines[-1].pop()
                lines.append([ '***SECTION***', prevTerm ])

        lines[-1].append(term)

# Strip out releated topics.
for line in lines:
    # Mutate list in place.  Only call index if there to prevent error.
    if 'RELATED' in line:
        index = line.index('RELATED')
        while len(line) > index:
            line.pop()

# Strip leading content before either 'GLOSSARY' or '1.13' (right column appears first in copy/paste, sigh).
while len(lines) > 0:
    text = ' '.join(lines[0])
    if ('GLOSSARY This glossary provides' in text) or ('1.13 TIMING' in text):
        break
    lines = lines[1:]

# Strip index page.
for i in range(len(lines)):
    if 'INDEX' in lines[i]:
        text = ' '.join(lines[i])

# Print distilled content.
for line in lines:
    if line[0] in ['***SECTION***', '***SUBSECTION***', '***QA***']:
        print(' '.join(line[1:]))

#EOF
