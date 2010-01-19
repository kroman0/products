Introduction
============

quintagroup.mobileextender package is designed for extend Documents, Events and 
containers with additional 'Mobile Content' field. This field may contain
alternative content in mobile presentation of the object.

If some content was added to the mentioned field, on object creation and/or
edition - such objects will be marked with qintagroup.mobile.interfaces.IMobile
interface. Such marked objects are taken into consideration by another
Quintagroup product - qPlongGoogleSitemaps for mobile sitemap creation.

There is *Manage Mobile Content* configlet, aimed to simplify object marking
with qintagroup.mobile.interfaces.IMobile interface, which allows you to
mark/unmark object with mentioned inteface.

Features
--------

On product installation *mobile_extender* File system directory view is added to
portal_skins, which contains alternative views for document, events and
containers. This views change presentation of mentioned objects by replacing
data from the 'Text' field to 'Mobile Content' one, in case it is not empty.

But this layer will not be added to the existent theme(s) by default, because
it lead to changing presentation mentioned objects for common (not-mobile) site
view.

So, to apply mentioned behavior you should manually add 'mobile_extender' layer to the 
theme, you intent to use as mobile one, just after 'custom' layer.

Also, after installation 'Manage Mobile Content' configlet is registered.

Requirements
------------

 * Plone 3.x

Dependency
----------

 * archetypes.schemaextender

Authors
-------

 * Anriy Mylenkyi
 * Volodymyr Cherepanyak
