#!/usr/bin/env bash

output_dir=$1
if [ -z $1 ]
then
    echo "Specify output direcotry path" 1>&2
    exit 1
fi
mkdir -p $output_dir
cd $output_dir

wget -q -O "index.html" 'https://news.ycombinator.com/news'

links=$(cat "index.html" \
    | hxclean \
    | hxselect 'a[href^="item"]' \
    | hxpipe \
    | grep 'item' \
    | sed 's/^.*id=\(.*\)$/\1/' \
    | sort \
    | uniq \
    | awk '{print "https://news.ycombinator.com/item?id=" $1}' \
    | xargs)

wget --wait 2 \
    --retry-on-http-error=503 \
    --no-verbose \
    --content-disposition \
    $links

rename 's/item\?id=//' ./*

