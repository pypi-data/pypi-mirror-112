#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rel_titles.py
"""Collection of religious titles."""
import bs4
import requests
import unicodedata
from bs4 import BeautifulSoup


def rel_titles() -> list:
    try:
        with open('./persontitles/religious_titles.txt', mode='r', encoding='utf-8') as fin:  # noqa
            REL_TITLES = fin.read().split('\n')
    except FileNotFoundError:
        REL_TITLES = religious_titles()
        with open('./persontitles/religious_titles.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in REL_TITLES))

    return REL_TITLES


def religious_titles() -> list:
    soup = get_soup()
    lines = get_less_lines(soup)

    return lines


def get_soup() -> bs4.element.NavigableString:
    data = requests.get('https://de.wikipedia.org/wiki/Liste_religi%C3%B6ser_Amts-_und_Funktionsbezeichnungen')  # noqa
    soup = BeautifulSoup(data.text, 'lxml')

    return soup


def get_less_lines(soup):
    lines = []
    for li in soup.find_all('li'):
        a = li.find('a')
        try:
            lines.append(a.get_text())
            lines.append(li.get_text())
        except AttributeError:
            pass

    counter = 0
    for i, line in enumerate(lines):
        if line.startswith('Papst'):
            counter = i
            break
    lines = lines[counter:]

    counter = 0
    for i, line in enumerate(lines):
        if line.startswith('Panchen Rinpoche'):
            counter = i
            break
    lines = lines[:counter + 1]

    return lines


def normalize_degrees(degrees) -> list:
    normalized_degrees = []
    for degree in degrees:
        degree = unicodedata.normalize('NFKD', degree.strip())
        degree = degree.strip()
        if degree not in normalized_degrees:
            normalized_degrees.append(degree)

    return normalized_degrees


if __name__ == '__main__':
    titles = religious_titles()
    for i, title in enumerate(titles):
        print(i, title)
