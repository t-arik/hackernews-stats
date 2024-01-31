import sys
import argparse
import re
import sqlite3
import bs4
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('input_dir', type=Path, help='Path to input directory \
                    containing the html files (e.g. data/2024-01-30-20-00/). \
                    note that the directory name serves as a index for the \
                    captured_at field of the database.')
parser.add_argument('database', type=Path, help='Path to a sqlite3 database file')
args = parser.parse_args()
input_dir: Path = args.input_dir
database_file: Path = args.database

def error(*args):
    print(*args, file=sys.stderr)
    exit(1)

# Check input
if not input_dir.is_dir():
    error(f'Error: {input_dir} is not a directory')

if not database_file.is_file():
    error(f'Error: {database_file} is not a file')

index_file = input_dir / 'index.html'

if not index_file.is_file():
    error(f'Error: {index_file} is not a file')

def main():
    item_files = list(input_dir.iterdir())
    item_files.remove(index_file)
    if len(item_files) < 30:
        error(f'Error: {input_dir} does not contain enough item files {len(item_files)}/30')

    # Parse the files
    index_html = bs4.BeautifulSoup(index_file.read_text(), 'lxml')
    parsed_headlines = list(get_headlines(index_html))
    parsed_items = []
    for item_file in item_files:
        item_html = bs4.BeautifulSoup(item_file.read_text(), 'lxml')
        item = get_item(item_html)
        parsed_items.append(item)

    # Write to database
    headline_rows = list(map(headline_to_tuple, parsed_headlines))
    item_rows = list(map(item_to_tuple, parsed_items))
    comment_rows = []
    for item in parsed_items:
        comment_rows.extend(map(comment_to_tuple, item['comments']))

    con = sqlite3.connect(args.database)
    cur = con.cursor()
    cur.executemany('INSERT INTO news_page VALUES (?,?,?,?,?,?,?,?,?,?)', headline_rows)
    cur.executemany('INSERT INTO item_page VALUES (?,?,?,?,?,?,?,?)', item_rows)
    cur.executemany('INSERT INTO comment VALUES (?,?,?,?,?,?,?,?,?)', comment_rows)
    con.commit()


def get_headlines(html):
    for news_item in html.find_all('tr', class_='athing'):
        headline = {}
        headline['id'] = news_item['id']
        headline['captured_at'] = input_dir.name
        headline['rank'] = news_item.find('span', class_='rank').text.strip('.')
        headline['title'] = news_item.find('span', class_='titleline').a.text
        headline['site'] = news_item.find('span', class_='titleline').a['href']
        headline['timestamp'] = news_item.next_sibling.find('span', class_='age')['title']
        headline['age'] = news_item.next_sibling.find('span', class_='age').a.text
        author = news_item.next_sibling.find('a', class_='hnuser')
        if author != None:
            headline['author'] = author.text
        else: headline['author'] = None
        points = news_item.next_sibling.find('span', class_='score')
        if points != None:
            headline['points'] = points.text.split()[0]
        else: headline['points'] = None
        comments = news_item.next_sibling.find('a', string=re.compile('comments'))
        if comments != None:
            headline['comments'] = comments.text.split()[0]
        else: headline['comments'] = None
        yield headline

def get_item(html):
    item = {}
    item['id'] = html.body.find('tr', class_="athing")['id']
    item['captured_at'] = input_dir.name
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
        result['captured_at'] = input_dir.name
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
    return item


def headline_to_tuple(headline):
    keys = ['id', 'captured_at', 'timestamp', 'rank', 'title',
            'site', 'age', 'points', 'author', 'comments']
    return tuple(headline[key] for key in keys)

def item_to_tuple(item):
    keys = ['id', 'captured_at', 'title', 'link', 'description',
            'points', 'user', 'comment_count']
    return tuple(item[key] for key in keys)

def comment_to_tuple(item):
    keys = ['id', 'captured_at', 'index', 'indent', 'user',
            'timestamp', 'age', 'content', 'item_id']
    return tuple(item[key] for key in keys)

if __name__ == '__main__':
    main()
