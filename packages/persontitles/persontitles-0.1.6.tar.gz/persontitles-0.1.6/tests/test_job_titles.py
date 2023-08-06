#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_job_titles.py
"""Tests for academic degrees."""
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))),
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)),
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from context import job_titles  # noqa


def test_no_file():
    try:
        os.remove('./persontitles/data/job_titles.txt')
    except FileNotFoundError:
        pass
    JOB_TITLES = job_titles.job_titles()
    assert isinstance(JOB_TITLES, dict)


def test_titles_is_dict_of_lists():
    JOB_TITLES = job_titles.job_titles()
    assert isinstance(JOB_TITLES, dict)
    assert isinstance(JOB_TITLES["German"], list)
    assert isinstance(JOB_TITLES["English"], list)
