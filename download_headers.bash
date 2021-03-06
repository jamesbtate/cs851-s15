#!/bin/bash -e
if [ -z "$1" ]
then
    echo "This program requires an argument: tweet id"
    exit -1
fi
for file in tweets2/$1/url.*
do
    #echo "$file"
    index=$(echo "$file" | grep -o "[0-9]\+$")
    url=$(cat $file)
    #echo "$url"
    curl -I -L -m 60 "$url" > "tweets2/$1/headers.$index" 2>&1
done
