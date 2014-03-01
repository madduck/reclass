==================
reclass to-do list
==================

Common set of classes
---------------------
A lot of the classes I have set up during the various stages of development of
|reclass| are generic. It would probably be sensible to make them available as
part of |reclass|, to give people a common baseline to work from, and to
ensure a certain level of consistency between users.

This could also provide a more realistic example to users on how to use
|reclass|.

Testing framework
-----------------
There is rudimentary testing in place, but it's inconsistent. I got
side-tracked into discussions about the philosphy of mocking objects. This
could all be fixed and unified.

Also, storage, outputters, CLI and adapters have absolutely no tests yet…

The testing framework should also incorporate the example classes mentioned
above.

Configurable file extension
---------------------------
Right now, ``.yml`` is hard-coded. This could be exported to the
configuration file, or even given as a list, so that ``.yml`` and ``.yaml``
can both be used.

Actually, I don't think this is such a good idea. If we create too many
options right now, it'll be harder to unify later. Please also see `issue #17
<https://github.com/madduck/reclass/issues/17`_ for a discussion about this.

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

On the other hand, providing CMS-specific data to reclass will make people
depend on it, meaning Salt cannot be used with multiple tools anymore.

The way to deal with that would be to map grains, facts, whatever the CMS
calls them, to a shared naming scheme/taxonomy, but that's a painful task,
I think. It would mean, however, that even templates could be shared between
CMSs if they only use the data provided by reclass (i.e. grains/facts become
pillar data).

Membership information
----------------------
It would be nice if |reclass| could provide e.g. the Nagios master node with
a list of clients that define it as their master. That would short-circuit
Puppet's ``storeconfigs`` and Salt's ``mine``.

The way I envision this currently is to provide something I call "inventory
queries". For instance, the Nagios master node's reclass data would contain
the following (``$[…]`` would denote interpolation to create a list, a bit
like list comprehension)::

  parameters:
    nagios:
      hosts: $[nagios:master == SELF.nodename]

This would cause |reclass| to iterate the inventory and generate a list of all
the nodes that define a parameter ``nagios:master`` whose value equals to the
name of the current node.

This could be greatly simplified. For instance, we could simply limit
comparisons against the name of the current node and just specify

::

  $[nagios:master]

which would be expanded to a list of node names whose pillar data includes
``${nagios:master}`` that matches the current node's name.

Or it could be made arbitrarily complex and flexible, e.g. any of the
following::

  $[nagios:master == SELF.nodename]                  # replace with nodename
  $[nagios:master == SELF.nodename | nodename]       # name replacement value
  $[nagios:master == SELF.nodename | nagios:nodeid]  # replace with pillar data
  $[x:nagios:nodeid foreach x | x:nagios:master == SELF.nodename]
  …

I'd rather not code this up from scratch, so I am looking for ideas for reuse…

Configuration file lookup improvements
--------------------------------------
Right now, the adapters and the CLI look for the :doc:`configuration file
<configfile>` in a fixed set of locations. On of those derives from
``OPT_INVENTORY_BASE_URI``, the default inventory base URI (``/etc/reclass``).
This should probably be updated in case the user changes the URI.

Furthermore, ``$CWD`` and ``~`` might not make a lot of sense in all
use-cases.

However, this might be better addressed by the following point:

Adapter class hierarchy
-----------------------
At the moment, adapters are just imperative code. It might make more sense to
wrap them in classes, which customise things like command-line and config file
parsing.

One nice way would be to generalise configuration file reading, integrate it
with command-line parsing, and then allow the consumers (the adapters) to
configure them, for instance, in the Salt adapter::

  config_proxy = ConfigProxy()
  config_proxy.set_configfile_search_path(['/etc/reclass', '/etc/salt'])
  config_proxy.lock_config_option('output', 'yaml')

The last call would effectively remove the ``--output`` config option from the
CLI, and yield an error (or warning) if the option was encountered while
parsing the configuration file.

Furthermore, the class instances could become long-lived and keep a reference
to a storage proxy, e.g. to prevent having to reload storage on every request.

Node lists
----------
Class mappings are still experimental, and one of the reasons I am not too
happy with them right now is that one would still need to provide node files
for all nodes for ``inventory`` invocations. This is because class mappings
can assign classes based on patterns or regular expressions, but it is not
possible to turn a pattern or regular expression into a list of valid nodes.

`Issue #9 <https://github.com/madduck/reclass/issues/9>`_ contains a lengthy
discussion on this. At the moment, I am unsure what the best way forward is.

Inventory filters
-----------------
As described in `issue #11 <https://github.com/madduck/reclass/issues/11>`_:
provide a means to limit the enumeration of the inventory, according to node
name patterns, or using classes white-/blacklists.

.. include:: substs.inc
