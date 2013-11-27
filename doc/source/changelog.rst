=========
ChangeLog
=========

========= ========== ========================================================
Version   Date       Changes
========= ========== ========================================================
                     * Introduce class mappings (see :doc:`operations`)
                       (closes: #5)
                     * Fix parameter interpolation across merged lists
                       (closes: #13).
                     * Caching of classes for performance reasons, especially
                       during the inventory runs
                     * yaml_fs: nodes may be defined in subdirectories
                       (closes: #10).
                     * Classes and nodes URI must not overlap anymore
                     * Class names must not contain spaces
1.1       2013-08-28 Salt adapter: fix interface to include minion_id, filter
                     output accordingly; fixes master_tops
1.0.2     2013-08-27 Fix incorrect versioning in setuptools
1.0.1     2013-08-27 Documentation updates, new homepage
1.0       2013-08-26 Initial release
========= ========== ========================================================
