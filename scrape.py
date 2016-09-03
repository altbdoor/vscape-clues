#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer

import json
import re


coord_page = 'http://vscape.wikidot.com/clue-scrolls'
misc_page = 'http://vscape.wikidot.com/wiki:treasure-trails-guide'
clue_list = []

# coord
with urlopen(coord_page) as response:
    strainer = SoupStrainer(class_='wiki-content-table')
    soup = BeautifulSoup(response.read(), 'html.parser', parse_only=strainer)
    coord_table = soup.find(class_='wiki-content-table')

rows = coord_table.find_all('tr', recursive=True)
for row in rows[1:]:
    cols = row.find_all('td', recursive=False)

    query = cols[1].text.lower().replace('\n', ' ')
    query = query.replace(' degrees ', '.').replace(' minutes ', ' ')
    query = re.sub(r' ([a-z])[a-z]+', r'\1', query)

    img_node = cols[0].find_all('a', recursive=False)

    clue_list.append({
        'type': 'coordinate',
        'query': query,
        'img_s': img_node[0].img['src'],
        'img_l': img_node[0]['href'],
        'desc': cols[2].text.replace('\n', ' '),
        'extra': {
            'img_mini_s': img_node[1].img['src'],
            'img_mini_l': img_node[1]['href'],
        },
    })


# misc
with urlopen(misc_page) as response:
    strainer = SoupStrainer(id='page-content')
    soup = BeautifulSoup(response.read(), 'html.parser', parse_only=strainer)
    misc_div = soup.find(id='page-content')

misc_tables = misc_div.find_all(class_='wiki-content-table', recursive=True)

misc_anagram = misc_tables[:2]
misc_cryptic = misc_tables[2:5]
misc_map = misc_tables[5:]

for table in misc_anagram:
    rows = table.find_all('tr', recursive=True)

    for row in rows:
        cols = row.find_all('td', recursive=False)

        clue_list.append({
            'type': 'anagram',
            'query': cols[0].em.text.replace(' ', '').lower(),
            'img_s': cols[2].a.img['src'],
            'img_l': cols[2].a['href'],
            'desc': cols[1].text.replace('\n', ' '),
        })

for table in misc_cryptic:
    rows = table.find_all('tr', recursive=True)

    for row in rows:
        cols = row.find_all('td', recursive=False)

        clue_list.append({
            'type': 'cryptic',
            'query': cols[0].em.text,
            'img_s': cols[2].a.img['src'],
            'img_l': cols[2].a['href'],
            'desc': cols[1].text.replace('\n', ' '),
        })

for table in misc_map:
    rows = table.find_all('tr', recursive=True)

    for row in rows:
        cols = row.find_all('td', recursive=False)
        first_col_info = cols[0].text

        clue_list.append({
            'type': 'map',
            'query': 'm' + re.search(r'ID (\d+)', first_col_info).group(1),
            'img_s': cols[2].a.img['src'],
            'img_l': cols[2].a['href'],
            'desc': cols[1].text.replace('\n', ' '),
            'extra': {
                'img_mini_s': cols[0].a.img['src'],
                'img_mini_l': cols[0].a['href'],
            },
        })

f = open('clue.json', 'w')
f.truncate()
f.write(json.dumps(clue_list))
f.close()
