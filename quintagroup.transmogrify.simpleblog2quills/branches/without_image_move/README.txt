quintagroup.transmogrifier.simpleblog2quills
============================================

Overview
--------

Configuration of collective.transmogrifier pipeline for blog migration from 
SimpleBlog to QuillsEnabled.

Installation
------------

See docs/INSTALL.txt for installation instructions.

Supported Plone versions and migration instructions
---------------------------------------------------

This package was designed to work and tested on next Plone versions:

 - Plone 2.1 / Plone 2.5

    SimpleBlog_ plone product is required.

 - Plone 3

    QuillsEnabled_ plone product is required. Install 
    quintagroup.transmogrifier.simpleblog2quills this product in QuickInstaller 
    (this will enable 'Large Folder' content type).

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
.. _QuillsEnabled: http://plone.org/products/quills
.. _Bohdan Koval: mailto:koval@quintagroup.com
.. _Quintagroup: http://quintagroup.com/
