Introduction
============

This package designed for extend Documents, Events and containers with additional
'Mobile Content' field. This field may contains alternative content in mobile
presentation of the object.

On creation and/or editing an object, if some content added to mentioned field, -
object marks with qintagroup.mobile.interfaces.IMobile interface. Object marked
with this interface take into consideration by other Quintagroup product -
qPlongGoogleSitemaps for mobile sitemap creation. For simplifying object marking
with qintagroup.mobile.interfaces.IMobile interface there is
*Manage Mobile Content* configlet, which alows you to mark/unmark object with
mentioned inteface.

On installation to portal_skins added *mobile_extender* File system directory
view, which contains alternative views for document, events and containers.
But this layer not added to existent themes by default because it lead to
changing presentation of mentioned objects with data from 'Mobile Content'
or if it empty - from the 'Text' field. So to apply mentioned behavior you
should add manually 'mobile_extender' layer to theme, which you design to use as
mobile one, just after 'custom' layer.

On installation also registered 'Manage Mobile Content' configlet and 

Installs: using 'Add/Remove Product' section on 'Site Setup' page.
Depends on: 'archetypes.schemaextender' package.
