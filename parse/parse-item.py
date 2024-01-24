#!/usr/bin/env python
import argparse
import pathlib
import typing
import bs4
import json

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('captured_at', type=str)
parser.add_argument('-d', '--database', type=pathlib.Path,
                    help='Path to a sqlite3 database file')
parser.add_argument('-j', '--json', type=argparse.FileType('w'))
parser.add_argument('-y', '--assume-yes', action='store_true')
args = parser.parse_args()


html: typing.Any = bs4.BeautifulSoup(args.infile, 'html.parser')

item = {}
item['id'] = html.body.find('tr', class_="athing")['id']
item['captured_at'] = args.captured_at
title = html.body.find('span', class_="titleline")
if title != None:
    item['title'] = title.a.text
else: item['title'] = None
item['link'] = html.head.find('link', rel='canonical')['href']
toptext = html.body.find('div', class_='toptext')
item['description'] = toptext and toptext.text
subline = html.body.find('span', class_='subline')
item['points'] = None
item['user'] = None
item['comment_count'] = None
if subline != None:
    item['points'] = subline.find('span', class_='score').text.split()[0]
    item['comment_count'] = subline.find_all('a')[-1].text.split()[0]
    user = subline.find('a', class_='hnuser')
    if user != None:
        item['user'] = user.text

item['comments'] = []

for idx, comment in enumerate(html.find_all('tr', class_='athing comtr')):
    result = {}
    result['id'] = comment['id']
    result['captured_at'] = args.captured_at
    result['index'] = idx
    result['indent'] = comment.find('td', class_='ind')['indent']
    user = comment.find('a', class_='hnuser')
    if user != None:
        result['user'] = user.text
    else: result['user'] = None
    result['timestamp'] = comment.find('span', class_='age')['title']
    result['age'] = comment.find('span', class_='age').a.text
    content = comment.find('div', class_='comment').span
    if content != None:
        if content.div != None:
            content.div.extract()
        result['content'] = content.text
    else: result['content'] = None
    result['item_id'] = item['id']
    item['comments'].append(result)


def item_to_tuple(item):
    keys = ['id', 'captured_at', 'title', 'link', 'description',
            'points', 'user', 'comment_count']
    return tuple(item[key] for key in keys)


def comment_to_tuple(item):
    keys = ['id', 'captured_at', 'index', 'indent', 'user',
            'timestamp', 'age', 'content', 'item_id']
    return tuple(item[key] for key in keys)


def write_to_db(item, comments):
    import sqlite3
    item_row = item_to_tuple(item)
    comment_rows = list(map(comment_to_tuple, comments))
    con = sqlite3.connect(args.database)
    cur = con.cursor()
    cur.execute('INSERT INTO item_page VALUES (?,?,?,?,?,?,?,?)', item_row)
    cur.executemany('INSERT INTO comment VALUES (?,?,?,?,?,?,?,?,?)', comment_rows)
    con.commit()


if args.database:
    if args.assume_yes or input(f'Write to {args.database}? y/n') == 'y':
        write_to_db(item, item['comments'])

if args.json:
    import json
    json.dump(item, args.json, indent=2)
