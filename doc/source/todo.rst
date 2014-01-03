==================
reclass to-do list
==================

Common set of classes
---------------------
A lot of the classes I have set up during the various stages of development of
|reclass| are generic. It would probably be sensible to make them available as
part of |reclass|, to give people a common baseline to work from, and to
ensure a certain level of consistency between users.

Testing framework
-----------------
There is rudimentary testing in place, but it's inconsistent. I got
side-tracked into discussions about the philosphy of mocking objects. This
could all be fixed and unified.

Also, storage, outputters, CLI and adapters have absolutely no tests yet…

Configurable file extension
---------------------------
Right now, ``.yml`` is hard-coded. This could be exported to the
configuration file, or even given as a list, so that ``.yml`` and ``.yaml``
can both be used.

Verbosity, debugging
--------------------
Verbose output and debug logging would be a very useful addition to help
people understand what's going on, where data are being changed/merged, and to
help solve problems.

Data from CMS for interpolation
-------------------------------
Depending on the CMS in question, it would be nice if |reclass| had access to
the host-specific data (facts, grains, etc.) and could use those in parameter
interpolation. I can imagine this working for Salt, where the ``grains``
dictionary (and results from previous external node classifiers) is made
available to the external node classifiers, but I am not convinced this will
be possible in Ansible and Puppet.

Ideally, |reclass| could unify the interface so that even templates can be
shared between the various CMS.

Membership information
----------------------
It would be nice if |reclass| could provide e.g. the Nagios master node with
a list of clients that define it as their master. That would short-circuit
Puppet's ``storeconfigs`` and Salt's ``mine``.

Configuration file lookup improvements
--------------------------------------
Right now, the adapters and the CLI look for the :doc:`configuration file
<configfile>` in a fixed set of locations. On of those derives from
``OPT_INVENTORY_BASE_URI``, the default inventory base URI (``/etc/reclass``).
This should probably be updated in case the user changes the URI.

Furthermore, ``$CWD`` and ``~`` might not make a lot of sense in all
use-cases.

Class subdirectories
--------------------
It would be nice syntactic sugar to allow classes to sit in subdirectories,
such that ``ssh.server`` would load a class in …/ssh/server.yml (assuming
``yaml_fs``).

See `this pull request for a discussion about it <https://github.com/madduck/reclass/pull/12>`_.

.. include:: substs.inc
