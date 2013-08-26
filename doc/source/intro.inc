|reclass| is an "external node classifier" (ENC) as can be used with
automation tools, such as `Puppet`_, `Salt`_, and `Ansible`_. It is also
a stand-alone tool for merging data sources recursively.

The purpose of an ENC is to allow a system administrator to maintain an
inventory of nodes to be managed, completely separately from the configuration
of the automation tool. Usually, the external node classifier completely
replaces the tool-specific inventory (such as ``site.pp`` for Puppet,
``ext_pillar``/``master_tops`` for Salt, or ``/etc/ansible/hosts``).

With respect to the configuration management tool, the ENC then fulfills two
jobs:

- it provides information about groups of nodes and group memberships
- it gives access to node-specific information, such as variables

|reclass| allows you to define your nodes through class inheritance, while
always able to override details further up the tree (i.e. in more specific
nodes). Think of classes as feature sets, as commonalities between nodes, or
as tags. Add to that the ability to nest classes (multiple inheritance is
allowed, well-defined, and encouraged), and you can assemble your
infrastructure from smaller bits, eliminating duplication and exposing all
important parameters to a single location, logically organised. And if that
isn't enough, |reclass| lets you reference other parameters in the very
hierarchy you are currently assembling.
