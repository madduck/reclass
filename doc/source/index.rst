================================================
reclass — Recursive external node classification
================================================
.. include:: intro.inc

Releases and source code
------------------------
The latest released |reclass| version is |release|. Please have a look at the
:doc:`change log <changelog>` for information about recent changes.

For now, |reclass| is hosted `on Github`_, and you may clone it with the
following command::

  git clone https://github.com/madduck/reclass.git

Please see the :doc:`install instructions <install>` for information about
distribution packages and tarballs.

.. _on Github: https://github.com/madduck/reclass

Community
---------
There is a `mailing list`_, where you can bring up anything related to
|reclass|.

.. _mailing list: http://lists.pantsfullofunix.net/listinfo/reclass

For real-time communication, please join the ``#reclass`` IRC channel on
``irc.oftc.net``.

If you're using `Salt`_, you can also ask your |reclass|-and-Salt-related
questions on the mailing list, ideally specifying "reclass" in the subject of
your message.

Licence
-------
|reclass| is © 2007–2014 by martin f. krafft and released under the terms of
the `Artistic Licence 2.0`_.

Contents
--------
These documents aim to get you started with |reclass|:

.. toctree::
   :maxdepth: 2

   install
   concepts
   operations
   usage
   refs
   manpage
   configfile
   salt
   ansible
   puppet
   hacking
   todo
   changelog

About the name
--------------
"reclass" stands for **r**\ ecursive **e**\ xternal node **class**\ ifier,
which is somewhat of a misnomer. I chose the name very early on, based on the
recursive nature of the data merging. However, to the user, a better paradigm
would be "hierarchical", as s/he does not and should not care too much about
the implementation internals. By the time that I realised this, unfortunately,
`Hiera`_ (Puppet-specific) had already occupied this prefix. Oh well. Once you
start using |reclass|, you'll think recursively as well as hierarchically at
the same time. It's really quite simple.

..
  Indices and tables
  ==================

  * :ref:`genindex`
  * :ref:`modindex`
  * :ref:`search`

.. include:: extrefs.inc
.. include:: substs.inc
