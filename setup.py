#!/usr/bin/env python

import sys
import os
from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(
    name = 'bottle-matplotlib',
    version = '0.1.0',
#    url = 'http://github.com/bottlepy/bottle-extras/',
    description = 'Matplotlib figure png generation for Bottle.',
    author = 'Malte Marquarding',
    author_email = 'Malte.Marquarding@csiro.au',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_matplotlib'
    ],
    requires = [
        'bottle (>=0.9)',
        'matplotlib'
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass = {'build_py': build_py}
)
