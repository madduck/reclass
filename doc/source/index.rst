================================================
reclass — Recursive external node classification
================================================
.. include:: intro.inc

Contents
--------
These documents aim to get you started with |reclass|:

.. toctree::
   :maxdepth: 2

   install
   concepts
   operations
   usage
   manpage
   configfile
   salt
   ansible
   puppet
   hacking
   todo

Community
---------
Currently, there exists only an IRC channel, ``#reclass`` on ``irc.oftc.net``,
where you may stop by to ask questions. When usage grows, I'll set up
a mailing list. If you're using `Salt`_, you can also ask your
|reclass|-related questions on the mailing list, ideally specifying
"reclass" in the subject of your message.

Source code
-----------
For now, |reclass| is hosted `on Github`_, and you may clone it with the
following command::

  git clone https://github.com/madduck/reclass.git

.. _on Github: https://github.com/madduck/reclass

Licence
-------
|reclass| is © 2007–2013 by martin f. krafft and released under the terms of
the `Artistic Licence 2.0`_.

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
