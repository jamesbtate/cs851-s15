#!/bin/bash -e
if [ -z "$1" ]
then
    echo "This program requires an argument: tweet id"
    exit -1
fi
for file in tweets/$1/url.*
do
    #echo "$file"
    index=$(echo "$file" | grep -o "[0-9]\+$")
    url=$(cat $file)
    dir="tweets/$1/content.$index"
    mkdir -p "$dir"
    #cd "$dir"
    #echo "$url"
    wget -t 2 -T 30 -E -e robots=off --trust-server-names -U 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4' -P "$dir/" "$url" > "$dir/wget.output" 2>&1
    #XZ_OPT=-9 tar cJf "${dir}.tar.xz" "$dir"
    #rm -rf "$dir"
done
