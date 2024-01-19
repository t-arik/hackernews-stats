#!/usr/bin/env bash
if [ -z "$1" ] && [ ! -d "$1" ]; then
    echo "Usage: $0 <data_dir>"
    exit 1
fi

ls $1 | cut -d- -f1-3 | sort | uniq -c
