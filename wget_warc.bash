#!/bin/bash
# $1 should be file with two columns:
#   first column is id of URI
#   second column is URI
# $2 should be directory where WARCs will be stored
if [ $# -ne 2 ]
then
    echo "Usage: $0 ids_and_uris_file save_dir"
    exit -1
fi
count=0
while read line
do
    count=$((count + 1))
    echo "$count"
    id=$(echo "$line" | cut -d' ' -f 1)
    uri=$(echo "$line" | cut -d' ' -f 2)
    wget --warc-file="$2/$id" -p -l 1 -H -e robots=off -U 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4' -P "garbage/" "$uri" > "$2/${id}.wget.output" 2>&1
done < $1
