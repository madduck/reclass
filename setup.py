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

setup(
    name = RECLASS_NAME,
    description = DESCRIPTION,
    version = VERSION,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    license = LICENCE,
    url = URL,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'reclass = reclass.cli:main',
            'reclass-salt = reclass.adapters.salt:cli',
            'reclass-ansible = reclass.adapters.ansible:cli'
        ]
    },
    install_requires = ['pyyaml'],
    setup_requires = ['nose'],
)
