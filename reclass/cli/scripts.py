#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

'''
Shell Scripts
-------------

This module defines functions for use as entry points, registered with entries
in ``console_scripts`` in ``setup.py``. Each function assembles and arg/option
parser and command structure with ``argh``, then dispatches those commands.
The commands (functions) are sourced from ``reclass.cli.cmd``.

'''
import sys, posix
import argh

from reclass.errors import ReclassException
from .cmd import nodeinfo, inventory, salt, ansible


p = argh.ArghParser()

def main():
    '''
    Entry point for ``reclass`` shell script, registered with setup.py. Dispatch
    commands ``nodeinfo`` and ``inventory``.

    '''
    try:
        argh.dispatch_commands([nodeinfo, inventory])
    except ReclassException, e:
        e.exit_with_message(sys.stderr)
    sys.exit(posix.EX_OK)


def reclass_salt():
    '''
    Entry point for ``reclass-salt`` shell script, registered with setup.py.
    Dispatch the ``salt`` command.

    '''
    try:
        p = argh.ArghParser()
        argh.set_default_command(p, salt)
        p.dispatch()
    except ReclassException, e:
        e.exit_with_message(sys.stderr)
    sys.exit(posix.EX_OK)


def reclass_ansible():
    '''
    Entry point for ``reclass-ansible`` shell script, registered with setup.py
    Dispatch the ``ansible`` command.

    '''
    try:
        p = argh.ArghParser()
        argh.set_default_command(p, ansible)
        p.dispatch()
    except ReclassException, e:
        e.exit_with_message(sys.stderr)
    sys.exit(posix.EX_OK)


