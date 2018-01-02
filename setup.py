#!/usr/bin/env python3
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="python-teamcymru",
    version="0.1.0",
    description=("Python wrapper for IP to ASN mapping initiative of team-cymru.org"),
    long_description=long_description,
    packages=find_packages(exclude=['docs', 'tests']),
    py_modules=['teamcymru'],
    tests_require=[
        "pytest>=3.3"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6'
    ]
)
