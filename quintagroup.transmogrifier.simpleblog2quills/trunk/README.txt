quintagroup.transmogrifier.simpleblog2quills Package Readme
=========================

Overview
--------

Configuration of collective.transmogrifier pipeline for migrating SimpleBlog
blog to Quills/QuillsEnabled content.

Installation
------------

See docs/INSTALL.txt for installation instructions.

Supported Plone versions
------------------------

This package was designed to work and tested on next Plone versions:

 - Plone 2.1

    SimpleBlog_ plone product is required.

 - Plone 3

    Quills_ or QuillsEnabled plone product is required. When migrating to 
    QuillsEnabled please edit transmogrifier import pipeline configuration file
    located in quintagroup/transmogrifier/simpleblog2quills/import.cfg (comments
    in that file will guide you through necessary modifications).


Running tests
-------------

    Run next command:

    bin/instance test -s quintagroup.transmogrifier.simpleblog2quills \
        -m test_import

Credits
-------

Design and development
   `Bohdan Koval`_ at Quintagroup_

.. _Quills: http://plone.org/products/quills
.. _SimpleBlog: http://plone.org/products/simpleblog
.. _Bohdan Koval: mailto:koval@quintagroup.com
.. _Quintagroup: http://www.quintagroup.com/
