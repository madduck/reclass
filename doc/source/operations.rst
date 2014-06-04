==================
reclass operations
==================

YAML FS storage
---------------
While |reclass| has been built to support different storage backends through
plugins, currently only the ``yaml_fs`` storage backend exists. This is a very
simple, yet powerful, YAML-based backend, using flat files on the filesystem
(as suggested by the ``_fs`` postfix).

``yaml_fs`` works with two directories, one for node definitions, and another
for class definitions. The two directories must not be the same, nor can one
be a parent of the other.

Files in those directories are YAML-files, specifying key-value pairs. The
following three keys are read by |reclass|:

============ ================================================================
Key          Description
============ ================================================================
classes      a list of parent classes
appliations  a list of applications to append to the applications defined by
             ancestors. If an application name starts with ``~``, it would
             remove this application from the list, if it had already been
             added — but it does not prevent a future addition.
             E.g. ``~firewalled``
parameters   key-value pairs to set defaults in class definitions, override
             existing data, or provide node-specific information in node
             specifications.
             \
             By convention, parameters corresponding to an application
             should be provided as subkey-value pairs, keyed by the name of
             the application, e.g.::

                applications:
                - ssh.server
                parameters:
                  ssh.server:
                    permit_root_login: no
environment  only relevant for nodes, this allows to specify an "environment"
             into which the node definition is supposed to be place.
============ ================================================================

Classes files may reside in subdirectories, which act as namespaces. For
instance, a class ``ssh.server`` will result in the class definition to be
read from ``ssh/server.yml``. Specifying just ``ssh`` will cause the class
data to be read from ``ssh/init.yml`` or ``ssh.yml``. Note, however, that only
one of those two may be present.

Nodes may also be defined in subdirectories. However, node names (filename)
must be unique across all subdirectories, and |reclass| will exit with an
error if a node is defined multiple times. Subdirectories therefore really
only exist for the administrator's local data structuring. They may be used in
mappings (see below) to tag additional classes onto nodes.

Data merging
------------
|reclass| has two modes of operation: node information retrieval and inventory
listing. The second is really just a loop of the first across all defined
nodes, and needs not be further described.

When retrieving information about a node, |reclass| first obtains the node
definition from the storage backend. Then, it iterates the list of classes
defined for the node and recursively asks the storage backend for each class
definition (unless already cached).

Next, |reclass| recursively descends each class, looking at the classes it
defines, and so on, until a leaf node is reached, i.e. a class that references
no other classes.

Now, the merging starts. At every step, the list of applications and the set
of parameters at each level is merged into what has been accumulated so far.

Merging of parameters is done "deeply", meaning that lists and dictionaries
are extended (recursively), rather than replaced. However, a scalar value
*does* overwrite a dictionary or list value. While the scalar could be
appended to an existing list, there is no sane default assumption in the
context of a dictionary, so this behaviour seems the most logical. Plus, it
allows for a dictionary to be erased by overwriting it with the null value.

After all classes (and the classes they reference) have been visited,
|reclass| finally merges the applications list and parameters defined for the
node into what has been accumulated during the processing of the classes, and
returns the final result.

Wildcard/Regexp mappings
------------------------
Using the :doc:`configuration file <configfile>`, it is also possible to
provide a list mappings between node names and classes. For instance::

  class_mappings:
    - \* default
    - /^www\d+/ webserver
    - \*.ch hosted@switzerland another_class_to_show_that_it_can_take_lists

This will assign the ``default`` class to all nodes (make sure to escape
a leading asterisk (\*) to keep YAML happy), ``webserver`` to all nodes named
``www1`` or ``www999``, and ``hosted-in-switzerland`` to all nodes whose names
end with ``.ch`` (again, note the escaped leading asterisk). Multiple classes
can be assigned to each mapping by providing a space-separated list (class
names cannot contain spaces anyway).

.. warning::

  The class mappings do not really belong in the configuration file, as they
  are data, not configuration inmformation. Therefore, they are likely going
  to move elsewhere, but I have not quite figured out to where. Most likely,
  there will be an additional file, specified in the configuration file, which
  then lists the mappings.

Note that mappings are not designed to replace node definitions. Mappings can
be used to pre-populate the classes of existing nodes, but you still need to
define all nodes (and if only to allow them to be enumerated for the
inventory).

The mapped classes can also contain backreferences when regular expressions
are used, although they need to be escaped, e.g.::

  class_mappings:
    - /\.(\S+)$/ tld-\\1

Furthermore, since the outer slashes ('/') are used to "quote" the regular
expression, *any* slashes within the regular expression must be escaped. For
instance, the following class mapping assigns a ``subdir-X`` class to all
nodes that are defined in a subdirectory (using yaml_fs)::

  class_mappings:
    - /^([^\/]+)\// subdir-\\1

Parameter interpolation
------------------------
Parameters may reference each other, including deep references, e.g.::

  parameters:
    location: Munich, Germany
    motd:
      header: This node sits in ${location}
    for_demonstration: ${motd:header}
    dict_reference: ${motd}

After merging and interpolation, which happens automatically inside the
storage modules, the ``for_demonstration`` parameter will have a value of
"This node sits in Munich, Germany".

Types are preserved if the value contains nothing but a reference. Hence, the
value of ``dict_reference`` will actually be a dictionary.

You should now be ready to :doc:`use reclass <usage>`!

.. include:: substs.inc
