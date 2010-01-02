quintagroup.transmogrify.pfm2pfg Package Readme
=================================================

Overview
--------

Configuration of collective.transmogrifier pipeline for migrating 
PloneFormMailer content to PloneFormGen content

Installation
------------

See docs/INSTALL.txt for installation instructions.

Supported Plone versions
------------------------

This package was designed to work and tested on next Plone versions:

 - Plone 2.1.5

    To run it you need to comment registration in ``configure.zcml`` of
    PloneFormGen dependent components. That is because Plone 2.1.5 runs on
    Zope 2.8, which includes Zope X3.0 and that version of zope doesn't support
    'zcml:condition' attribute in ZCML configuration files.
 
 - Plone 3.1.5

Running tests
-------------

 - Plone 2.1.5

    Remove or rename ``test_import.py`` in package's tests directory because
    this test module depends on Plone 3.1. And run next:

    bin/instance test --libdir path/to/quintagroup.transmogrify.pfm2pfg

 - Plone 3.1.5

    Run next command:

    bin/instance test -s quintagroup.transmogrify.pfm2pfg -m test_import

Credits
-------

Design and development
   `Bohdan Koval`_ at Quintagroup_

.. _Bohdan Koval: mailto:koval@quintagroup.com
.. _Quintagroup: http://www.quintagroup.com/
