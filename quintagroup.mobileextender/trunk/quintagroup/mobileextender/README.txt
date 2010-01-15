Introduction
============

quintagroup.mobileextender package is designed for extend Documents, Events and 
containers with additional 'Mobile Content' field. This field may contain alternative 
content in mobile presentation of the object.

If some content was added to the mentioned field, on object creation and/or edition - 
such objects will be marked with qintagroup.mobile.interfaces.IMobile interface. 

Such marked objects are taken into consideration by another Quintagroup product - 
qPlongGoogleSitemaps for mobile sitemap creation. There is *Manage Mobile Content* 
configlet, aimed to simplify object marking with qintagroup.mobile.interfaces.IMobile 
interface, which allows you to mark/unmark object with mentioned inteface.

Features
--------

On product installation *mobile_extender* File system directory view is added to 
portal_skins, which contains alternative views for document, events and containers.

But this layer will not be not added to the existent theme by default settings, 
because it might lead to changing presentation of mentioned objects with data from 
'Mobile Content' field, or in case it is empty - from the 'Text' field. 

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