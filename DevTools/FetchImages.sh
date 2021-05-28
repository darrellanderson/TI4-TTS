#!/bin/bash
#cat TS_Save_22.json | sed -e "s/[\\]n/∑/g" | tr '∑' '\n' | grep '["'\'']http' | sed -e 's/.*\(http[^"'\'' ]*\).*/\1/' | sort | uniq
while read -r line
do
    filename=$( printf "%s" "$line" | tr -cs 'a-zA-Z0-9' '_' )
    #echo $filename
    curl "$line" -o "/Users/darrell/t.images/$filename"
done
