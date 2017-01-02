#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

from reclass.version import *
from setuptools import setup, find_packages

# use consistent encoding of readme for pypi
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

ADAPTERS = ['salt', 'ansible']
console_scripts = ['reclass = reclass.cli:main']
console_scripts.extend('reclass-{0} = reclass.adapters.{0}:cli'.format(i)
                       for i in ADAPTERS)

setup(
    name = RECLASS_NAME,
    description = DESCRIPTION,
    long_description=long_description,
    version = VERSION,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = MAINTAINER,
    maintainer_email = MAINTAINER_EMAIL,
    license = LICENCE,
    url = URL,
    packages = find_packages(exclude=['*tests']), #FIXME validate this
    entry_points = { 'console_scripts': console_scripts },
    install_requires = ['pyyaml'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: Artistic License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='enc ansible salt'
)
