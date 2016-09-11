#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests",
]

test_requirements = [
    "vcrpy"
]

setup(
    name='python_mojepanstwo',
    version='0.1.0',
    description=" A Python client for mojePaństwo API.",
    long_description=readme + '\n\n' + history,
    author="Adam Dobrawy",
    author_email='naczelnik@jawnosc.tk',
    url='https://github.com/ad-m/python_mojepanstwo',
    packages=[
        'python_mojepanstwo',
    ],
    package_dir={'python_mojepanstwo':
                 'python_mojepanstwo'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='python_mojepanstwo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
