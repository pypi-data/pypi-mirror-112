#!/usr/bin/env python
# -*- coding: utf-8 -*-
# salutations.py
"""Collection of salutations like "Mr." or "Frau"."""


def salutations() -> list:
    with open('./persontitles/resources/salutations.txt', mode='r', encoding='utf-8') as fin:  # noqa
        SALUTATIONS = [salut.strip() for salut in fin.read().split('\n') if salut.strip()]  # noqa

    return SALUTATIONS


if __name__ == '__main__':
    SALUTATIONS = salutations()
    for i, salut in enumerate(SALUTATIONS):
        print(i, salut)
