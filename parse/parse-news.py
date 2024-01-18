#!/usr/bin/env python

import argparse
import re
import sys
import bs4
import json

parser = argparse.ArgumentParser(prog='HackerNewsFrontpageParser')
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))
parser.add_argument('--run', action='store_true') # safety switch
args = parser.parse_args()

html = bs4.BeautifulSoup(args.infile, 'html.parser')

records = []

for news_item in html.find_all('tr', class_='athing'):
    record = {}
    record['id'] = news_item['id']
    record['rank'] = news_item.find('span', class_='rank').text.strip('.')
    record['title'] = news_item.find('span', class_='titleline').a.text
    record['site'] = news_item.find('span', class_='titleline').a['href']

    points = news_item.next_sibling.find('span', class_='score')
    if points != None:
        record['points'] = points.text.split()[0]

    author = news_item.next_sibling.find('a', class_='hnuser')
    if author != None:
        record['author'] = author.text

    record['timestamp'] = news_item.next_sibling.find('span', class_='age')['title']
    record['age'] = news_item.next_sibling.find('span', class_='age').a.text

    comments = news_item.next_sibling.find('a', string=re.compile('comments'))
    if comments != None:
        record['comments'] = comments.text.split()[0]

    records.append(record)

filename = args.outfile.name
if args.run:
    json.dump(records, args.outfile, indent=2)
else:
    print(f'Would write to {filename}. Use --run to actually write.', file=sys.stderr)
