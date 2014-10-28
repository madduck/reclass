==========================
reclass configuration file
==========================
|reclass| can read some of its configuration from a file. The file is
a YAML-file and simply defines key-value pairs.

The configuration file can be used to set defaults for all the options that
are otherwise configurable via the command-line interface, so please use the
``--help`` output of |reclass| (or the :doc:`manual page <manpage>`) for
reference. The command-line option ``--nodes-uri`` corresponds to the key
``nodes_uri`` in the configuration file. For example::

  storage_type: yaml_fs
  pretty_print: True
  output: json
  inventory_base_uri: /etc/reclass
  nodes_uri: ../nodes

|reclass| first looks in the current directory for the file called
``reclass-config.yml`` (see ``reclass/defaults.py``) and if no such file is
found, it looks in ``$HOME``, then in ``/etc/reclass``, and then "next to" the
``reclass`` script itself, i.e. if the script is symlinked to
``/srv/provisioning/reclass``, then the the script will try to access
``/srv/provisioning/reclass-config.yml``.

Note that ``yaml_fs`` is currently the only supported ``storage_type``, and
it's the default if you don't set it.

Adapters may implement their own lookup logic, of course, so make sure to read
their documentation (for :doc:`Salt <salt>`, for :doc:`Ansible <ansible>`, and
for :doc:`Puppet <puppet>`).

.. include:: substs.inc
