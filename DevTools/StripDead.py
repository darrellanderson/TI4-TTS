#!/usr/bin/python

# Naive dead code elimination: break input into chunks, anonymous and per-function.
# Create a tree from root functions to all accessable, eliminate dead functions.
# (Something like this MUST exist out there, I couldn't find one.  Boo.)
# For simplicity do not attempt to suppress code inside --[[ ]] comments.

import re
import sys

# -----------------------------------------------------------------------------

def newBlock():
    return {
        'lines' : [],
        'local' : None,
        'functionName' : None,
        'functionCalls' : set()
    }

def error(message):
    sys.exit('ERROR: ' + message)

# -----------------------------------------------------------------------------

functionNamePattern = re.compile(r'^(local )?function ([^(]*)\(')
functionCallPattern = re.compile(r'(CrLua\.[\._A-Za-z0-9]*)\(')

# In-order blocks.  Each block is { lines: [], function: name, calls: set }
blocks = [ newBlock() ]
insideFunction = False

for line in sys.stdin:
    # Reject multi-line comments (could ignore, but safer to require none).
    if line.find('--[[') != -1:
        error('multi-line comments not supported')

    # Is this a function definition?
    match = functionNamePattern.match(line)
    if match:
        # Function definition.  Assign to block.
        if insideFunction:
            error('^function definition inside function (bad indent?)')
        insideFunction = True

        # If the block does not end with a comment start a new one.
        block = blocks[-1]
        if len(block['lines']) > 0 and not block['lines'][-1].startswith('--'):
            blocks.append(newBlock())
            block = blocks[-1]

        functionName = match.group(2)
        if block['functionName']:
            error('block already has function: ' + block['functionName'] + ' vs new ' + functionName)
        block['local'] = match.group(1)
        block['functionName'] = functionName
    else:
        # Not function definition, rememeber any function calls.
        for functionCall in functionCallPattern.findall(line):
            block['functionCalls'].add(functionCall)

    # If outside a function, start a new block when encountering a non-comment.
    # This groups LuaDoc comments with adjacent functions.
    if not insideFunction and not line.startswith('--'):
        blocks.append(newBlock())

    # Add line to current block.
    block = blocks[-1]
    block['lines'].append(line.rstrip())

    # Start new block AFTER closing a function.
    if line.startswith('end'):
        if not insideFunction:
            error('^end not inside function')
        insideFunction = False
        blocks.append(newBlock())

# -----------------------------------------------------------------------------

# Map from functionName to functionCall set.
reaches = {}
toExplore = set()
for block in blocks:
    functionName = block['functionName']
    if functionName:
        reaches[functionName] = block['functionCalls']
        if not functionCallPattern.match(functionName + '()') or functionName.find('__') != -1:
            toExplore.add(functionName)
    else:
        toExplore |= block['functionCalls']

reachable = set()
visited = set()
while toExplore:
    functionName = toExplore.pop()
    if not functionName in visited:
        visited.add(functionName)
        reachable.add(functionName)
        if functionName in reaches:
            toExplore |= reaches[functionName]

# -----------------------------------------------------------------------------

for block in blocks:
    functionName = block['functionName']
    if not functionName or functionName in reachable:
        for line in block['lines']:
            print line
