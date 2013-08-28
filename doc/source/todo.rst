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

Default classes
---------------
Through the configuration file, it should be possible to define a set of
default classes that are applied to all nodes (before anything else).

This would be covered by the next point:

Wildcards, regexp→class mapping
-------------------------------
I envision the ability to define mappings between regexps and classes, e.g.::

    /^www\d+/   →  webservers
    /\.ch\./    →  hosted@switzerland

These classes would be applied before a YAML file matching the actual hostname
would be read and merged.

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

Node environments
-----------------
At least Salt and Puppet support the notion of "environments", but the Salt
adapter just puts everything into the "base" environment at the moment.

Part of the reason that multiple environments aren't (yet) supported is
because I don't see the use-case (anymore) with |reclass|. If you still see
a use-case, then please help me understand it and let's figure out a good way
to introduce this concept into |reclass|.

Membership information
----------------------
It would be nice if |reclass| could provide e.g. the Nagios master node with
a list of clients that define it as their master. That would short-circuit
Puppet's ``storeconfigs`` and Salt's ``mine``.

.. include:: substs.inc
