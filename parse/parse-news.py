#!/usr/bin/env python

import argparse
import re
import bs4
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('captured_at', type=str)
parser.add_argument('-d', '--database', type=pathlib.Path,
                    help='Path to a sqlite3 database file')
parser.add_argument('-j', '--json', type=argparse.FileType('w'))
parser.add_argument('-y', '--assume-yes', action='store_true')
args = parser.parse_args()

html = bs4.BeautifulSoup(args.infile, 'html.parser')

articles = []

for news_item in html.find_all('tr', class_='athing'):
    article = {}
    article['id'] = news_item['id']
    article['captured_at'] = args.captured_at
    article['rank'] = news_item.find('span', class_='rank').text.strip('.')
    article['title'] = news_item.find('span', class_='titleline').a.text
    article['site'] = news_item.find('span', class_='titleline').a['href']
    article['timestamp'] = news_item.next_sibling.find('span', class_='age')['title']
    article['age'] = news_item.next_sibling.find('span', class_='age').a.text

    author = news_item.next_sibling.find('a', class_='hnuser')
    if author != None:
        article['author'] = author.text
    else: article['author'] = None

    points = news_item.next_sibling.find('span', class_='score')
    if points != None:
        article['points'] = points.text.split()[0]
    else: article['points'] = None

    comments = news_item.next_sibling.find('a', string=re.compile('comments'))
    if comments != None:
        article['comments'] = comments.text.split()[0]
    else: article['comments'] = None

    articles.append(article)


def to_values(article):
    keys = ['id', 'captured_at', 'timestamp', 'rank', 'title',
            'site', 'age', 'points', 'author', 'comments']
    return tuple(article[key] for key in keys)


if args.database:
    import sqlite3
    if args.assume_yes or input(f'Write to {args.database}? y/n') == 'y':
        rows = list(map(to_values, articles))
        con = sqlite3.connect(args.database)
        cur = con.cursor()
        cur.executemany('INSERT INTO news_page VALUES (?,?,?,?,?,?,?,?,?,?)', rows)
        con.commit()

if args.json:
    import json
    json.dump(articles, args.json, indent=2)

