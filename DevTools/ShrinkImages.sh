#!/bin/bash

while read -r line
do
    filename=$( printf "%s" "$line" | tr -cs 'a-zA-Z0-9' '_' )
    src="/Users/darrell/t.images/$filename"
    dst="/Users/darrell/t.images_jpg_best/$filename"
    sips -s format jpeg -s formatOptions best "$src" --out "$dst"
done
