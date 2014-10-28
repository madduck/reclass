================
reclass concepts
================
|reclass| assumes a node-centric perspective into your inventory. This is
obvious when you query |reclass| for node-specific information, but it might not
be clear when you ask |reclass| to provide you with a list of groups. In that
case, |reclass| loops over all nodes it can find in its database, reads all
information it can find about the nodes, and finally reorders the result to
provide a list of groups with the nodes they contain.

Since the term "groups" is somewhat ambiguous, it helps to start off with
a short glossary of |reclass|-specific terminology:

============ ==============================================================
Concept      Description
============ ==============================================================
node         A node, usually a computer in your infrastructure
class        A category, tag, feature, or role that applies to a node
             Classes may be nested, i.e. there can be a class hierarchy
application  A specific set of behaviour to apply
parameter    Node-specific variables, with inheritance throughout the class
             hierarchy.
============ ==============================================================

A class consists of zero or more parent classes, zero or more applications,
and any number of parameters.

A class name must not contain spaces.

A node is almost equivalent to a class, except that it usually does not (but
can) specify applications.

When |reclass| parses a node (or class) definition and encounters a parent
class, it recurses to this parent class first before reading any data of the
node (or class). When |reclass| returns from the recursive, depth first walk, it
then merges all information of the current node (or class) into the
information it obtained during the recursion.

Furthermore, a node (or class) may define a list of classes it derives from,
in which case classes defined further down the list will be able to override
classes further up the list.

Information in this context is essentially one of a list of applications or
a list of parameters.

The interaction between the depth-first walk and the delayed merging of data
means that the node (and any class) may override any of the data defined by
any of the parent classes (ancestors). This is in line with the assumption
that more specific definitions ("this specific host") should have a higher
precedence than more general definitions ("all webservers", which includes all
webservers in Munich, which includes "this specific host", for example).

Here's a quick example, showing how parameters accumulate and can get
replaced.

  All "unixnodes" (i.e. nodes who have the ``unixnode`` class in their
  ancestry) have ``/etc/motd`` centrally-managed (through the ``motd``
  application), and the `unixnode` class definition provides a generic
  message-of-the-day to be put into this file.

  All descendants of the class ``debiannode``, a descendant of ``unixnode``,
  should include the Debian codename in this message, so the
  message-of-the-day is overwritten in the ``debiannodes`` class.

  The node ``quantum.example.org`` (a `debiannode`) will have a scheduled
  downtime this weekend, so until Monday, an appropriate message-of-the-day is
  added to the node definition.

  When the ``motd`` application runs, it receives the appropriate
  message-of-the-day (from ``quantum.example.org`` when run on that node) and
  writes it into ``/etc/motd``.

At this point it should be noted that parameters whose values are lists or
key-value pairs don't get overwritten by children classes or node definitions,
but the information gets merged (recursively) instead.

Similarly to parameters, applications also accumulate during the recursive
walk through the class ancestry. It is possible for a node or child class to
*remove* an application added by a parent class, by prefixing the application
with `~`.

Finally, |reclass| happily lets you use multiple inheritance, and ensures that
the resolution of parameters is still well-defined. Here's another example
building upon the one about ``/etc/motd`` above:

  ``quantum.example.org`` (which is back up and therefore its node definition
  no longer contains a message-of-the-day) is at a site in Munich. Therefore,
  it is a child of the class ``hosted@munich``. This class is independent of
  the ``unixnode`` hierarchy, ``quantum.example.org`` derives from both.

  In this example infrastructure, ``hosted@munich`` is more specific than
  ``debiannode`` because there are plenty of Debian nodes at other sites (and
  some non-Debian nodes in Munich). Therefore, ``quantum.example.org`` derives
  from ``hosted@munich`` _after_ ``debiannodes``.

  When an electricity outage is expected over the weekend in Munich, the admin
  can change the message-of-the-day in the ``hosted@munich`` class, and it
  will apply to all hosts in Munich.

  However, not all hosts in Munich have ``/etc/motd``, because some of them
  are of class ``windowsnode``. Since the ``windowsnode`` ancestry does not
  specify the ``motd`` application, those hosts have access to the
  message-of-the-day in the node variables, but the message won't get used…

  … unless, of course, ``windowsnode`` specified a Windows-specific
  application to bring such notices to the attention of the user.

It's also trivial to ensure a certain order of class evaluation. Here's
another example:

  The ``ssh.server`` class defines the ``permit_root_login`` parameter to ``no``.

  The ``backuppc.client`` class defines the parameter to ``without-password``,
  because the BackupPC server might need to log in to the host as root.

  Now, what happens if the admin accidentally provides the following two
  classes?

  - ``backuppc.client``
  - ``ssh.server``

  Theoretically, this would mean ``permit_root_login`` gets set to ``no``.

  However, since all ``backuppc.client`` nodes need ``ssh.server`` (at least
  in most setups), the class ``backuppc.client`` itself derives from
  ``ssh.server``, ensuring that it gets parsed before ``backuppc.client``.

  When |reclass| returns to the node and encounters the ``ssh.server`` class
  defined there, it simply skips it, as it's already been processed.

Now read about :doc:`operations`!

.. include:: substs.inc
