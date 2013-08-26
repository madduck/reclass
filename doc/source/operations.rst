==================
reclass operations
==================

Data merging
------------
While |reclass| has been built to support different storage backends through
plugins, currently only the ``yaml_fs`` storage backend exists. This is a very
simple, yet powerful, YAML-based backend, using flat files on the filesystem
(as suggested by the ``_fs`` postfix).

``yaml_fs`` works with two directories, one for node definitions, and another
for class definitions. It is possible to use a single directory for both, but
that could get messy and is therefore not recommended.

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
============ ================================================================

|reclass| starts out reading a node definition file, obtains the list of
classes, then reads the files corresponding to these classes, recursively
reading parent classes, and finally merges the applications list and the
parameters.

Merging of parameters is done recursively, meaning that lists and dictionaries
are extended (recursively), rather than replaced. However, a scalar value
*does* overwrite a dictionary or list value. While the scalar could be
appended to an existing list, there is sane default assumption in the context
of a dictionary, so this behaviour seems the most logical.

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
