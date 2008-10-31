quintagroup.transmogrifier.simpleblog2quills Package Readme
=========================

Overview
--------

Configuration of collective.transmogrifier pipeline for migrating SimpleBlog
content to Quills content.

Installation
------------

See docs/INSTALL.txt for installation instructions.

Supported Plone versions
------------------------

This package was designed to work and tested on next Plone versions:

 - Plone 3.1.5

    Quills_ plone product is required, now version 1.6 is supported.


Running tests
-------------

    Run next command:

    bin/instance test -s quintagroup.transmogrifier.simpleblog2quills \
        -m test_import

Credits
-------

Design and development
   `Bohdan Koval`_ at Quintagroup_

.. _Quills: http://plone.org/products/quills/releases/1.6/quills-1-6-beta1.tgz
.. _Bohdan Koval: mailto:koval@quintagroup.com
.. _Quintagroup: http://www.quintagroup.com/
