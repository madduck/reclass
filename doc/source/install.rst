============
Installation
============

For Debian users (including Ubuntu)
-----------------------------------
|reclass| has been `packaged for Debian`_. To use it, just install it with
APT::

  $ apt-get install reclass [reclass-doc]

.. _packaged for Debian: http://packages.debian.org/search?keywords=reclass

For ArchLinux users
-------------------
|reclass| is `available for ArchLinux`_, thanks to Niels Abspoel.
Dowload the tarball_ from ``aur`` or ``yaourt``::

  $ yaourt -S reclass

or::

  $ tar xvzf reclass-git.tar.gz
  $ cd reclass-git; makepkg
  $ sudo pacman -U reclass-git-<git-commit-hash>.tar.gz

.. _available for ArchLinux: https://aur.archlinux.org/packages/reclass-git/
.. _tarball: https://aur.archlinux.org/packages/re/reclass-git/reclass-git.tar.gz

Other distributions
-------------------
Developers of other distributions are cordially invited to package |reclass|
themselves and `write to the mailing list
<mailto:reclass@pantsfullofunix.net>`_ to have details included here. Or send
a patch!

From source
-----------
|reclass| is currently maintained `on Github
<http://github.com/madduck/reclass>`_, so to obtain the source, run::

  $ git clone https://github.com/madduck/reclass.git

or::

  $ git clone ssh://git@github.com:madduck/reclass.git

If you want a tarball, please `obtain it from the Debian archive`_.

.. _obtain it from the Debian archive: http://http.debian.net/debian/pool/main/r/reclass/

Before you can use |reclass|, you need to install it into a place where Python
can find it. The following step should install the package to ``/usr/local``::

  $ python setup.py install

If you want to install to a different location, use --prefix like so::

  $ python setup.py install --prefix=/opt/local

.. todo::

  These will install the ``reclass-salt`` and ``reclass-ansible`` adapters to
  ``$prefix/bin``, but they should go to ``$prefix/share/reclass``. How can
  setup.py be told to do so? It would be better for consistency if this was
  done "upstream", rather than fixed by the distros.

Just make sure that the destination is in the Python module search path, which
you can check like this::

  $ python -c 'import sys; print sys.path'

More options can be found in the output of

::

  $ python setup.py install --help
  $ python setup.py --help
  $ python setup.py --help-commands
  $ python setup.py --help [cmd]

If you just want to run |reclass| from source, e.g. because you are going to be
making and testing changes, install it in "development mode"::

  $ python setup.py develop

To uninstall (the rm call is necessary due to `a bug in setuptools`_)::

  $ python setup.py develop --uninstall
  $ rm /usr/local/bin/reclass*

`Uninstallation currently isn't possible`_ for packages installed to
/usr/local as per the above method, unfortunately. The following should do::

  $ rm -r /usr/local/lib/python*/dist-packages/reclass* /usr/local/bin/reclass*

.. _a bug in setuptools: http://bugs.debian.org/714960
.. _Uninstallation currently isn't possible: http://bugs.python.org/issue4673

.. include:: substs.inc
