#!/usr/bin/env bash
cd $(dirname "$0")

dir=$(date '+%Y-%m-%d-%H')
mkdir $dir && cd $dir

wget -q -O index.html 'https://news.ycombinator.com/news'

cat index.html \
    | hxclean \
    | hxselect 'a[href^="item"]' \
    | hxpipe \
    | grep 'item' \
    | sed 's/^.*id=\(.*\)$/\1/' \
    | sort \
    | uniq \
    | xargs -I {} wget -q -O '{}.html' 'https://news.ycombinator.com/item?id={}' \

echo "[$(date '+%Y-%m-%d-%H')] Downloaded $(ls -1 | wc -l) files from news.ycombinator.com." \
    >> ../log.txt
