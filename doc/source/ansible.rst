==========================
Using reclass with Ansible
==========================

.. warning::

  I was kicked out of the Ansible community, presumably for `asking the wrong
  questions`_, and therefore I have no interest in developing this adapter
  anymore. If you use it and have changes, I will take your patch.

.. _asking the wrong questions: https://github.com/madduck/reclass/issues/6

Quick start with Ansible
------------------------
The following steps should get you up and running quickly with |reclass| and
`Ansible`_. Generally, we will be working in ``/etc/ansible``. However, if you
are using a source-code checkout of Ansible, you might also want to work
inside the ``./hacking`` directory instead.

Or you can also just look into ``./examples/ansible`` of your |reclass|
checkout, where the following steps have already been prepared.

/…/reclass refers to the location of your |reclass| checkout.

.. todo::

  With |reclass| now in Debian, as well as installable from source, the
  following should be checked for path consistency…

#. Complete the installation steps described in the :doc:`installation section
   <install>`.

#. Symlink ``/usr/share/reclass/reclass-ansible`` (or wherever your distro put
   that file), or ``/…/reclass/reclass/adapters/ansible.py`` (if running from
   source) to ``/etc/ansible/hosts`` (or ``./hacking/hosts``).

#. Copy the two directories ``nodes`` and ``classes`` from the example
   subdirectory in the |reclass| checkout to ``/etc/ansible``

   If you prefer to put those directories elsewhere, you can create
   ``/etc/ansible/reclass-config.yml`` with contents such as::

     storage_type: yaml_fs
     inventory_base_uri: /srv/reclass

   Note that ``yaml_fs`` is currently the only supported ``storage_type``, and
   it's the default if you don't set it.

#. Check out your inventory by invoking

   ::

     $ ./hosts --list

   which should return 5 groups in JSON format, and each group has exactly
   one member ``localhost``.

4. See the node information for ``localhost``::

     $ ./hosts --host localhost

   This should print a set of keys and values, including a greeting,
   a colour, and a sub-class called ``__reclas__``.

5. Execute some ansible commands, e.g.::

     $ ansible -i hosts \* --list-hosts
     $ ansible -i hosts \* -m ping
     $ ansible -i hosts \* -m debug -a 'msg="${greeting}"'
     $ ansible -i hosts \* -m setup
     $ ansible-playbook -i hosts test.yml

6. You can also invoke |reclass| directly, which gives a slightly different
   view onto the same data, i.e. before it has been adapted for Ansible::

     $ /…/reclass/reclass.py --pretty-print --inventory
     $ /…/reclass/reclass.py --pretty-print --nodeinfo localhost

   Or, if |reclass| is properly installed, just use the |reclass| command.

Integration with Ansible
------------------------
The integration between |reclass| and Ansible is performed through an adapter,
and needs not be of our concern too much.

However, Ansible has no concept of "nodes", "applications", "parameters", and
"classes". Therefore it is necessary to explain how those correspond to
Ansible. Crudely, the following mapping exists:

================= ===============
|reclass| concept Ansible concept
================= ===============
nodes             hosts
classes           groups
applications      playbooks
parameters        host_vars
================= ===============

|reclass| does not provide any ``group_vars`` because of its node-centric
perspective. While class definitions include parameters, those are inherited
by the node definitions and hence become node_vars.

|reclass| also does not provide playbooks, nor does it deal with any of the
related Ansible concepts, i.e. ``vars_files``, vars, tasks, handlers, roles, etc..

  Let it be said at this point that you'll probably want to stop using
  ``host_vars``, ``group_vars`` and ``vars_files`` altogether, and if only
  because you should no longer need them, but also because the variable
  precedence rules of Ansible are full of surprises, at least to me.

|reclass|' Ansible adapter massage the |reclass| output into Ansible-usable data,
namely:

- Every class in the ancestry of a node becomes a group to Ansible. This is
  mainly useful to be able to target nodes during interactive use of
  Ansible, e.g.::

    $ ansible debiannode@wheezy -m command -a 'apt-get upgrade'
      → upgrade all Debian nodes running wheezy

    $ ansible ssh.server -m command -a 'invoke-rc.d ssh restart'
      → restart all SSH server processes

    $ ansible mailserver -m command -a 'tail -n1000 /var/log/mail.err'
      → obtain the last 1,000 lines of all mailserver error log files

  The attentive reader might stumble over the use of singular words, whereas
  it might make more sense to address all ``mailserver*s*`` with this tool.
  This is convention and up to you. I prefer to think of my node as
  a (singular) mailserver when I add ``mailserver`` to its parent classes.

- Every entry in the list of a host's applications might well correspond to
  an Ansible playbook. Therefore, |reclass| creates a (Ansible-)group for
  every application, and adds ``_hosts`` to the name. This postfix can be
  configured with a CLI option (``--applications-postfix``) or in the
  configuration file (``applications_postfix``).

  For instance, the ssh.server class adds the ssh.server application to
  a node's application list. Now the admin might create an Ansible playbook
  like so::

    - name: SSH server management
      hosts: ssh.server_hosts              ← SEE HERE
      tasks:
        - name: install SSH package
          action: …
      …

  There's a bit of redundancy in this, but unfortunately Ansible playbooks
  hardcode the nodes to which a playbook applies.

  It's now trivial to apply this playbook across your infrastructure::

    $ ansible-playbook ssh.server.yml

  My suggested way to use Ansible site-wide is then to create a ``site.yml``
  playbook that includes all the other playbooks (which shall hopefully be
  based on Ansible roles), and then to invoke Ansible like this:

    ansible-playbook site.yml

  or, if you prefer only to reconfigure a subset of nodes, e.g. all
  webservers::

    $ ansible-playbook site.yml --limit webserver

  Again, if the singular word ``webserver`` puts you off, change the
  convention as you wish.

  And if anyone comes up with a way to directly connect groups in the
  inventory with roles, thereby making it unnecessary to write playbook
  files (containing redundant information), please tell me!

- Parameters corresponding to a node become ``host_vars`` for that host.

Variable interpolation
----------------------
Ansible allows you to include `Jinja2`_-style variables in parameter values::

  parameters:
    motd:
      greeting: Welcome to {{ ansible_fqdn }}!
      closing: This system is part of {{ realm }}
    dict_reference: {{ motd }}

However, in resolving this, Ansible casts everything to a string, so in this
example, ``dict_reference`` would be the string-representation of the
dictionary under the ``motd`` key [#string_casts]_. To get at facts (such as
``ansible_fqdn``), you still have to use this approach, but for pure parameter
references, I strongly suggest to use |reclass| interpolation instead, as it
supports deep references, does not clobber type information, and is more
efficient anyway::

  parameters:
    motd:
      greeting: Welcome to {{ ansible_fqdn }}!
      closing: This system is part of ${realm}
    dict_reference: ${motd}

Now you just need to specify realm somewhere. The reference can reside in
a parent class, while the variable is defined e.g. in the node definition.

And as expected, ``dict_reference`` now points to a dictionary, not
a string-representation thereof.

.. [#string_casts] I pointed this out to Michael Dehaan, Ansible's chief
   developer, but he denied this behaviour. When I tried to provide further
   insights, I found myself banned from the mailing list, apparently because
   I dared to point out flaws. If you care, you may look at
   https://github.com/madduck/reclass/issues/6 for more information.

.. include:: extrefs.inc
.. include:: substs.inc
