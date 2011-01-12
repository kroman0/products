Introduction
============

Plone Migration Tool for migrating content between two Plone websites that allows to export content
from one Plone website and import it into another one.

quintagroup.transmogrifier package includes Plone blueprints for collective.transmogrifier pipelines
that are used for exporting/importing Plone site content. So, quintagroup.transmogrifier package can 
be used as independent Plone Migration Tool by providing ways for handling content migration from one 
Plone site to another. This package overrides GenericSetup 'Content' step - so this package can be used
 out-the-box to migrate site content.

The included blueprints allow to:

 * quintagroup.transmogrifierreturn queried items from the catalog
 * create pipeline items from contents of Plone site folders
 * walk through different GenericSetup import contexts and yield items for every folder
 * generate and parse manifest files - listings of objects contained in some foldere in XML format
 * migrate properties for objects that inherit from OFS.PropertyManager.PropertyManager mixin class
 * use context sensitive components (adapters) to do needed corrections in data generated in previous sections
 * set references for content objects
 * migrate comments for site content
 * extract data from Archetypes file fields
 * apply stylesheet to some XML data stored on item. 

You can manage import/export procedure by configuring pipeline and appropriate blueprints in quintagroup.transmogrifier
configlet that appears after products installation.

Apart from standard Plone content types migration, quintagroup.transmogrifier allows to carry out migration of 
additional Plone content types. There are special packages used for such cases: these are 
quintagroup.transmogrifier.simpleblog2quills (allows blog migration from SimpleBlog to Quills) and 
quintagroup.transmogrifier.pfm2pfg (allows forms migration from PloneFromMailer to PloneFormGen).

Credits
-------

Design and development by:

* Bohdan Koval
* Andriy Mylenkyy
* Vitaliy Podoba
* Volodymyr Cherepanyak
* Myroslav Opyr