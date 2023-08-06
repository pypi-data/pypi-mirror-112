#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gov_jobs.py
"""Collection of (currently) German government job titles."""
import bs4
import requests
import unicodedata
from bs4 import BeautifulSoup
# from pprint import pprint


urls = [
    'http://www.besoldungstabelle.de/besoldungsgruppen_amtsbezeichnungen_besoldungstabelle'  # noqa
]


def gov_jobs() -> list:
    try:
        with open('./persontitles/data/gov_jobs.txt', mode='r', encoding='utf-8') as fin:  # noqa
            GOV_JOBS = fin.read().split('\n')
    except FileNotFoundError:
        GOV_JOBS = gov_job_titles()
        with open('./persontitles/data/gov_jobs.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in GOV_JOBS))

    return GOV_JOBS


def gov_job_titles() -> list:
    titles_1 = titles_url_1()
    print('titles_1')
    print(titles_1)
    job_titles = [ttle for ttle in set(titles_1)]  # noqa
    job_titles = change_first_word_to_female(job_titles)
    fem_male_collection = change_2_or_more_words_to_female(job_titles)

    return fem_male_collection


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
    print(lines)

    lines = lines[12:47]
    title_collection = []
    for line in lines:
        title = line.split(':')[-1]
        if '-Besoldung' not in title:
            title_collection.append(title.strip())

    ttle_collection = title_collection[:]
    title_collection = []
    for title in ttle_collection:
        titles = title.split(',')
        for ttle in titles:
            title_collection.append(ttle.strip())

    ttle_collection = title_collection[:]
    title_collection = []
    for title in ttle_collection:
        title = title.split('(')[0]
        title_collection.append(title.strip())

    ttle_collection = title_collection[:]
    title_collection = []
    for title in ttle_collection:
        if 'usw.' in title:
            title = title.split('usw.')[0]
        elif ' einer' in title:
            title = title.split(' einer')[0]
        elif 'ehem.' in title:
            title = title.split('ehem.')[-1]
        elif ' und' in title:
            title = title.split(' und')[0]
        title_collection.append(title.strip())

    title_collection = normalize_titles(title_collection)

    return title_collection


def normalize_titles(titles) -> list:
    normalized_titles = []
    for title in titles:
        title = unicodedata.normalize('NFKD', title.strip())
        title = title.strip()
        if title not in normalized_titles:
            normalized_titles.append(title)

    return normalized_titles


def change_first_word_to_female(titles) -> list:
    female_vers_added = []
    for title in titles:
        female_vers_added.append(title.strip())
        fields = title.split(' ')
        end = ' '.join(fields[1:])
        ttle = fields[0]
        fem_title = change_to_female_variant(ttle) + ' ' + end
        while '  ' in fem_title:
            fem_title = fem_title.replace('  ', ' ')
        fem_title = fem_title.strip()
        if fem_title not in female_vers_added:
            female_vers_added.append(fem_title)

    return female_vers_added


def change_to_female_variant(title) -> str:
    # need to normalize with NFC because otherwise "Präsident" will not be
    # recognized and even counted with 10 letters!
    ttle = unicodedata.normalize('NFC', title.strip())
    if ttle in ['Direktor', 'Konsul', 'Präsident', 'Chef', 'Kanzler', 'Sekretär']:  # noqa
        fem_title = ttle + 'in '
    elif ttle.endswith('ektor') or ttle.endswith('onsul') or\
        ttle.endswith('räsident') or ttle.endswith('hef') or\
        ttle.endswith('anzler') or ttle.endswith('ekretär') or\
        ttle.endswith('rofessor') or ttle.endswith('fleger') or\
        ttle.endswith('eister') or ttle.endswith('ührer') or\
        ttle.endswith('ommissar') or ttle.endswith('rinär') or\
        ttle.endswith('theker') or ttle.endswith('konservator') or\
        ttle.endswith('schafter') or ttle.endswith('stent'):  # noqa
        fem_title = ttle + 'in '
    elif ttle.endswith('rat'):
        fem_title = ttle[:-3] + 'rätin'
    elif ttle.endswith('arzt'):
        fem_title = ttle[:-4] + 'ärztin'
    elif ttle.endswith('walt'):
        fem_title = ttle[:-4] + 'wältin'
    elif ttle == 'Rat':
        fem_title = 'Rätin '
    elif ttle == 'Arzt':
        fem_title = 'Ärztin '
    else:
        fem_title = title

    return fem_title


def change_2_or_more_words_to_female(titles) -> list:
    female_vers_added = []
    for title in titles:
        # append the male versions and the female versions so far
        female_vers_added.append(title)

        fields = title.split(' ')
        if len(fields) > 1:
            male_ttle = fields[-1]
            male_ttle = unicodedata.normalize('NFC', male_ttle.strip())
            fem_ttle = change_to_female_variant(male_ttle)
            if male_ttle != fem_ttle:
                fem_title = change_to_female(fields) + ' ' + fem_ttle.strip()
                female_vers_added.append(fem_title)

    return female_vers_added


def change_to_female(fields) -> str:
    fields_wo_last_field = fields[:-1]
    fem_words = ''
    for field in fields_wo_last_field:
        if field.endswith('r'):
            field = field[:-1]
            fem_words = fem_words + field + ' '

    return fem_words.strip()


if __name__ == '__main__':
    titles = gov_job_titles()
    for i, title in enumerate(sorted(titles)):
        print(i, title)
