#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

# from setuptools import find_packages  # type: ignore
from setuptools import setup  # type: ignore


with open('README.rst') as readme_file:
    long_description = readme_file.read()

requirements = [
    'beautifulsoup4',
    'lxml',
    'requests',
]

test_requirements = [
    'pytest>=3',
]

setup(
    author='Oliver Stapel',
    author_email='hardy.ecc95@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX :: Linux',
        'Topic :: Other/Nonlisted Topic',
    ],
    description='Collections of academic degrees, job (and peer) titles, and salutations.',  # noqa
    install_requires=requirements,
    license='MIT license',
    long_description=long_description,
    long_description_content_type='text/x-rst',
#     include_package_data=True,
#     package_data={"persontitles": ["*.txt", "*.json"]},
    packages=['persontitles'],
#     packages=find_packages(
#         where='src',
#         include=['*.py'],
#         exclude=('tests',)
#     ),  # noqa
    keywords='person, titles, degrees',
    name='persontitles',
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/0LL13/persontitles',
    version='0.2.6',
    zip_safe=False,
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest-cov'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/0LL13/persontitles/issues',
        'Source': 'https://github.com/0LL13/persontitles',
    },
)
