=============
Using reclass
=============
.. todo::

  With |reclass| now in Debian, as well as installable from source, the
  following should be checked for path consistency…

For information on how to use |reclass| directly, call ``reclass --help``
and study the output, or have a look at its :doc:`manual page <manpage>`.

The three options, ``--inventory-base-uri``, ``--nodes-uri``, and
``--classes-uri`` together specify the location of the inventory. If the base
URI is specified, then it is prepended to the other two URIs, unless they are
absolute URIs. If these two URIs are not specified, they default to ``nodes``
and ``classes``. Therefore, if your inventory is in ``/etc/reclass/nodes`` and
``/etc/reclass/classes``, all you need to specify is the base URI as
``/etc/reclass`` — which is actually the default (specified in
``reclass/defaults.py``).

If you've installed |reclass| from source as per the :doc:`installation
instructions <install>`, try to run it from the source directory like this::

  $ reclass -b examples/ --inventory
  $ reclass -b examples/ --nodeinfo localhost

This will make it use the data from ``examples/nodes`` and
``examples/classes``, and you can surely make your own way from here.

On Debian-systems, use the following::

  $ reclass -b /usr/share/doc/reclass/examples/ --inventory
  $ reclass -b /usr/share/doc/reclass/examples/ --nodeinfo localhost

More commonly, however, use of |reclass| will happen indirectly, and through
so-called adapters. The job of an adapter is to translate between different
invocation paradigms, provide a sane set of default options, and massage the
data from |reclass| into the format expected by the automation tool in use.
Please have a look at the respective README files for these adapters, i.e.
for :doc:`Salt <salt>`, for :doc:`Ansible <ansible>`, and for :doc:`Puppet
<puppet>`.

.. include:: substs.inc
