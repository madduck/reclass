==================
Hacking on reclass
==================

Installation
------------
If you just want to run |reclass| from source, e.g. because you are going to be
making and testing changes, install it in "development mode"::

  python setup.py develop

Now the ``reclass`` script, as well as the adapters, will be available in
``/usr/local/bin``, and you can also invoke them directly from the source
tree.

To uninstall::

  python setup.py develop --uninstall

Discussing reclass
------------------
If you want to talk about |reclass|, use the `mailing list`_ or to find me on
IRC, in ``#reclass`` on ``irc.oftc.net``.

.. _mailing list: http://lists.pantsfullofunix.net/listinfo/reclass

Contributing to reclass
-----------------------
|reclass| is currently maintained `on Github
<http://github.com/madduck/reclass>`_.

Conttributions to |reclass| are very welcome. Since I prefer to keep a somewhat
clean history, I will not just merge pull request.

You can submit pull requests, of course, and I'll rebase them onto ``HEAD``
before merging. Or send your patches using ``git-format-patch`` and
``git-send-e-mail`` to `the mailing list
<reclass@lists.pantsfullofunix.net>`_.

I have added rudimentary unit tests, and it would be nice if you could submit
your changes with appropriate changes to the tests. To run tests, invoke

::

  $ make tests

in the top-level checkout directory. The tests are rather inconsistent, some
using mock objects, and only the datatypes-related code is covered. If you are
a testing expert, I could certainly use some help here to improve the
consistency of the existing tests, as well as their coverage.

Also, there is a Makefile giving access to PyLint and ``coverage.py`` (running
tests). If you run that, you can see there is a lot of work to be done
cleaning up the code. If this is the sort of stuff you want to do — by all
means — be my guest! ;)

There are a number of items on the :doc:`to-do list <todo>`, so if you are
bored…

If you have larger ideas, I'll be looking forward to discuss them with you.

.. include:: substs.inc
