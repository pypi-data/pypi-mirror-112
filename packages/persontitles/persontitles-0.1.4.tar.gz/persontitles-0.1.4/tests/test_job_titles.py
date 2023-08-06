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
    os.remove('./persontitles/job_titles.txt')
    JOB_TITLES = job_titles.job_titles()
    assert isinstance(JOB_TITLES, list)


def test_titles_is_list():
    JOB_TITLES = job_titles.job_titles()
    assert isinstance(JOB_TITLES, list)
