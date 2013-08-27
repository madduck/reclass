===============
reclass manpage
===============

Synopsis
--------
| |reclass| --help
| |reclass| *[options]* --inventory
| |reclass| *[options]* --nodeinfo=NODENAME

Description
-----------
.. include:: intro.inc

|reclass| will be used indirectly through adapters most of the time. However,
there exists a command-line interface that allows querying the database. This
manual page describes this interface.

Options
-------
Please see the output of ``reclass --help`` for the default values of these
options:

Database options
''''''''''''''''
-s, --storage-type        The type of storage backend to use
-b, --inventory-base-uri  The base URI to prepend to nodes and classes
-u, --nodes-uri           The URI to the nodes storage
-c, --classes-uri         The URI to the classes storage

Output options
''''''''''''''
-o, --output              The output format to use (yaml or json)
-y, --pretty-print        Try to make the output prettier

Modes
'''''
-i, --inventory           Output the entire inventory
-n, --nodeinfo            Output information for a specific node

Information
'''''''''''
-h, --help                Help output
--version                 Display version number

See also
--------
Please visit http://reclass.pantsfullofunix.net/ for more information about
|reclass|.

The documentation is also available from the ``./doc`` subtree in the source
checkout, or from ``/usr/share/doc/reclass-doc``.

.. include:: substs.inc
.. include:: extrefs.inc
