#!/usr/bin/env python
import argparse
import typing
import bs4
import json

parser = argparse.ArgumentParser(prog='HackerNewsItemParser')
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))
parser.add_argument('--run', action='store_true') # safety switch
args = parser.parse_args()

html: typing.Any = bs4.BeautifulSoup(args.infile, 'html.parser')

item = {}
item['title'] = html.body.find('span', class_="titleline").a.text
item['id'] = html.body.find('tr', class_="athing")['id']
item['link'] = html.head.find('link', rel='canonical')['href']
toptext = html.body.find('div', class_='toptext')
item['description'] = toptext and toptext.text
subline = html.body.find('span', class_='subline')
if subline != None:
    item['points'] = subline.find('span', class_='score').text.split()[0]
    item['user'] = subline.find('a', class_='hnuser').text
    item['comment_count'] = subline.find_all('a')[-1].text.split()[0]
item['comments'] = []

for idx, comment in enumerate(html.find_all('tr', class_='athing comtr')):
    record = {}
    record['id'] = comment['id']
    record['index'] = idx
    record['indent'] = comment.find('td', class_='ind')['indent']
    record['user'] = comment.find('a', class_='hnuser').text
    record['timestamp'] = comment.find('span', class_='age')['title']
    record['age'] = comment.find('span', class_='age').a.text
    content = comment.find('div', class_='comment').span
    if content.div != None:
        content.div.extract()
    record['content'] = content.text
    item['comments'].append(record)

filename = args.outfile.name
if args.run:
    json.dump(item, args.outfile, indent=2)
else:
    print(f'Would write to {filename}. Use --run to actually write.', file=sys.stderr)
