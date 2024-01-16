#!/usr/bin/env python

import argparse
import re
import csv
import bs4

parser = argparse.ArgumentParser(prog='HackerNewsFrontpageParser')
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))
args = parser.parse_args()

html = bs4.BeautifulSoup(args.infile, 'html.parser')
writer = csv.writer(args.outfile)

writer.writerow(['Rank', 'Title', 'Site', 'Points', 'Author', 'Timestamp', 'Age', 'Comments'])
for news_item in html.find_all('tr', class_='athing'):
    rank = news_item.find('span', class_='rank').text.strip('.')
    title = news_item.find('span', class_='titleline').a.text
    site = news_item.find('span', class_='titleline').a['href']

    points = news_item.next_sibling.find('span', class_='score')
    if points != None:
        points = points.text.split()[0]
    else:
        points = ""

    author = news_item.next_sibling.find('a', class_='hnuser')
    if author != None:
        author = author.text
    else:
        author = ""

    timestamp = news_item.next_sibling.find('span', class_='age')['title']
    age = news_item.next_sibling.find('span', class_='age').a.text

    comments = news_item.next_sibling.find('a', string=re.compile('comments'))
    if comments != None:
        comments = comments.text.split()[0]
    else:
        comments = ""

    writer.writerow([rank, title, site, points, author, timestamp, age, comments])

