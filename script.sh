#!/usr/bin/env bash
cd $(dirname "$0")

dirname="data/$(date '+%Y-%m-%d-%H-%M')"
mkdir -p $dirname

index='index.html'
wget -q -O "$dirname/$index" 'https://news.ycombinator.com/news'

links=$(cat "$dirname/$index" \
    | hxclean \
    | hxselect 'a[href^="item"]' \
    | hxpipe \
    | grep 'item' \
    | sed 's/^.*id=\(.*\)$/\1/' \
    | sort \
    | uniq \
    | awk '{print "https://news.ycombinator.com/item?id=" $1}' \
    | xargs)

wget -P \
    $dirname \
    --wait 2 \
    --retry-on-http-error=503 \
    --no-verbose \
    --content-disposition \
    --append-output='download.log' \
    $links

rename 's/item\?id=//' $dirname/*

