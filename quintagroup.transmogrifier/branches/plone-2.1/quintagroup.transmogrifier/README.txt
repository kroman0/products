***************************************
Export/import transmogrifier blueprints
***************************************

.. contents::

This package contains blueprints for collective.transmogrifier
pipelines, that may be used to export/import Plone site content.
It also overrides GenericSetup ``Content`` step so this package
can be used out-the-box to migrate site content.

Running test
************

On Plone 2.1.5 run all tests by executing next command (it's assumed thad this 
package is installed in buildout as development egg):

    bin/instance test --libdir path/to/quintagroup.transmogrifier

Credits
*******

Design and development
    `Bohdan Koval`_ at Quintagroup_

.. _Bohdan Koval: mailto:koval@quintagroup.com
.. _Quintagroup: http://www.quintagroup.com/
