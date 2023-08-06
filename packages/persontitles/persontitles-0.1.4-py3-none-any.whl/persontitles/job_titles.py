#!/usr/bin/env python
# -*- coding: utf-8 -*-
# job_titles.py
"""Collection of English and German job titles."""
import bs4
import json
import requests
# import sys
import unicodedata
from bs4 import BeautifulSoup
# from pprint import pprint


urls = [
    'https://www.nachrichten.at/wirtschaft/karriere/tipps/bewerbung/das-steckt-hinter-englischen-berufsbezeichnungen;art215506,3298147',  # noqa
    'https://www.xing.com/campus/de/job-search',
    'https://zety.com/blog/job-titles',
]


def job_titles() -> list:
    try:
        with open('./persontitles/job_titles.txt', mode='r', encoding='utf-8') as fin:  # noqa
            JOB_TITLES = fin.read().split('\n')
    except FileNotFoundError:
        JOB_TITLES = job_titles_mix()
        with open('./persontitles/job_titles.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in JOB_TITLES))

    return JOB_TITLES


def job_titles_mix() -> list:
    titles_1 = titles_url_1()
    titles_2 = titles_url_2()
    titles_3 = titles_url_3()
    job_titles = [ttle for ttle in set(titles_1) | set(titles_2) | set(titles_3)]  # noqa

    return job_titles


def get_soup(url) -> bs4.element.NavigableString:
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'lxml')

    return soup


def titles_url_1() -> list:
    url = urls[0]
    soup = get_soup(url)
    lines = []
    for p in soup.find_all('p'):
        lines.append(p.get_text(strip=True))

    lines = lines[5:87]
    title_collection = []
    for line in lines:
        titles = line.split('-')
        for title in titles:
            title_collection.append(title.strip())

    ttle_collection = title_collection[:]
    title_collection = []
    for title in ttle_collection:
        titles = title.split('/')
        for ttle in titles:
            title_collection.append(ttle.strip())

    ttle_collection = title_collection[:]
    title_collection = []
    for title in ttle_collection:
        titles = title.split(',')
        for ttle in titles:
            if ttle == 'Consultat':
                ttle = 'Consultant'
            elif 'Worker' in ttle:
                pass
            title_collection.append(ttle.strip())

    ttle_collection = title_collection[:]
    title_collection = []
    for title in ttle_collection:
        ttle = title.split('(')[0]
        title_collection.append(ttle.strip())

    title_collection = normalize_titles(title_collection)
    title_collection.remove('Head of...')

    return title_collection


def titles_url_2() -> list:
    titles = []
    url = urls[1]
    soup = get_soup(url)
    rawJ = soup.find('script')
# this ignores the json stuff and only makes use of splitting strings
    J = str(rawJ)
    J1 = J.split('var _env=')[-1]
    J2 = J1.split(';')[4]
    J3 = J2.split('var REDUX_STATE=')[-1]
    for line in J3.split(','):
        if line.startswith('"name"'):
            title = line.split(':')[-1]
            title = title[1:].split('"')[0]
            if title not in ['Arbeiter', 'Absolvent', 'Satz']:
                titles.append(title)

    return titles


def titles_url_3() -> list:
    titles = []
    url = urls[2]
    soup = get_soup(url)

# take a peek at the structure of those nested json dicts:
# https://stackoverflow.com/a/63151716/6597765
#     for i, rawJ in enumerate(soup.find_all('script', type="application/ld+json")):  # noqa
#         print("index:", i)
#         data = json.loads(rawJ.string)
#         for k, v in data.items():
#             print("key:", k)
#             print("value")
#             pprint(v)
#             print()

    rawJs = soup.find_all('script', type='application/ld+json')
    J1 = json.loads(rawJs[1].string)
    J2 = J1['@graph'][2]
    J3 = J2['articleBody']
    titles_ = J3.split('&amp;nbsp;')
    for i, title in enumerate(titles_):
        if i in [17, 35, 42, 51, 58, 66, 74, 81, 85, 92, 98, 103, 108, 113, 118, 123, 128, 133, 138, 144, 149, 152, 156, 159, 162, 165, 169, 172, 175, 179]:  # noqa
            titles.append(title.strip())

    titles_ = []
    for title in titles:
        title = title.split('\n')
        for ttle in title:
            titles_.append(ttle)

    titles = titles_[2:]
    titles_ = []
    titles = normalize_titles(titles)
    for title in titles:
        if '&amp;mdash;' in title:
            titles_.append(title.split('&amp;mdash;')[0])
            titles_.append(title.split('&amp;mdash;')[-1])
        elif '/' in title:
            titles_.append(title.split('/')[0].strip())
            titles_.append(title.split('/')[-1].strip())
        elif '(' in title:
            titles_.append(title.split('(')[0].strip())
            titles_.append(title.split('(')[-1][:-1].strip())
        elif '&amp;rsquo;' in title:
            title = title.replace('&amp;rsquo;', "'")
            titles_.append(title.strip())
        elif '&amp;amp;' in title:
            titles_.append(title.split('&amp;amp;')[0].strip())
            titles_.append(title.split('&amp;amp;')[-1].strip())
        else:
            titles_.append(title)

    titles = [title for title in set(titles_)]

#    for i, title in enumerate(sorted(titles)):
#        print(i, title)
#    sys.exit()

    return titles


def normalize_titles(titles) -> list:
    normalized_titles = []
    for title in titles:
        title = unicodedata.normalize('NFKD', title.strip())
        title = title.strip()
        if title not in normalized_titles:
            normalized_titles.append(title)

    return normalized_titles


if __name__ == '__main__':
    titles = job_titles_mix()
    for i, title in enumerate(sorted(titles)):
        print(i, title)
