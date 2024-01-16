#!/usr/bin/env bash
cat download.log | grep '^....-..-..' | cut -d' ' -f1 | sort | uniq -c
