quintagroup.transmogrifier.simpleblog2quills
============================================

Overview
--------

Configuration of collective.transmogrifier pipeline for migrating blog from 
SimpleBlog to Quills/QuillsEnabled.

Installation
------------

See docs/INSTALL.txt for installation instructions.

Supported Plone versions and migration instructions
---------------------------------------------------

This package was designed to work and tested on next Plone versions:

 - Plone 2.1

    SimpleBlog_ plone product is required. To migrate SimbleBlog to Quills this
    package must move all images and files, that were added somewhere in the
    blog to one centralized folder. That's why modifications of links to those
    images/files are needed and these are done automatically. There is only 
    problem with absolute links, because site URL isn't known. To make it possible
    to fix absolute links please edit export configuration file 'export.cfg',
    which is located in 'quintagroup/transmogrifier/simpleblog2quills' folder.
    Find in that file line that starts with "site-urls = " and change values
    that come after it to your site URL.

 - Plone 3

    Quills_ or QuillsEnabled_ plone product is required. When migrating blog to 
    QuillsEnabled please edit import configuration file 'import.cfg' located in
    'quintagroup/transmogrifier/simpleblog2quills' folder (comments in that file 
    will guide you through necessary modifications).

Running tests
-------------

 - Plone 3

    Run next command:

    bin/instance test -s quintagroup.transmogrifier.simpleblog2quills \
        -m test_import

Credits
-------

Design and development `Bohdan Koval`_ at Quintagroup_

.. _SimpleBlog: http://plone.org/products/simpleblog
.. _Quills: http://plone.org/products/quills
.. _QuillsEnabled: http://plone.org/products/quills
.. _Bohdan Koval: mailto:koval@quintagroup.com
.. _Quintagroup: http://quintagroup.com/
