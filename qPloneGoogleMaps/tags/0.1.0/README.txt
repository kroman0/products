Plone Google Maps

  Plone Google Maps (qPloneGoogleMaps) is a Google Maps view product
  for the Plone content management system which enables integration
  of Google Maps into Plone sites.

Plone Google Maps Features

   1. Due to qPloneGoogleMaps you can set up the latitude and longitude
      of your site objects and have their maps exhibited on your site.
   2. Any object with the latitude-longitude has an additional map
      portlet displaying this object. This portlet, in turn, has a
      template "Large screen". If you click on the large screen below
      the portlet, you will be able to see the full-size map of the
      page with its description.
   3. The folders containing objects with the latitude-longitude
      parameters have an additional display view - "maps view",
      which gives an opportunity to see the full-size map with all
      these objects.
   4. There is a new content type "Map" which can have other content
      types - "overlays". It enables the positioning of different
      objects on one map showing them with the markers of different
      colours.

Plone Google Maps Installation

    * Install qPloneGoogleMaps and geolocation as Zope products
    * Install these two products in your Plone instance with Quick
      Installer (Plone Control Panel ->Add/remove Products)

How To Use qPloneGoogleMaps

 Use Case 1

    Let's assume you need to show two objects (Plone pages) situated in
    one folder on one map.

      * Suppose you have a folder "School"
      * Create two pages for this folder ("School 1", "School 2")
      * Go to the page "School 1" and click on the tab "geolocation"
      * You will see a page with the latitude, longitude,zoom, type
        fields and an empty Google map. Fill in the fields which determine
        map displaying properties and then click on map for choosing
        marker position and then click the "Save" button
      * Do the same steps for the page "School 2"
      * Go to the folder "School"
      * Choose "maps view" from the "display" drop-down menu. You will
        see the map with both of these objects ("School 1", "School 2")
        marked with the markers. If you click on one of these markers
        you will see its name and description appear beside it (after
        the click on this name you will be taken to the page the marker
        displays) 

 Use Case 2

    Let's assume, you need to show many objects situated in different
    folders on one map.

      * Suppose, you have a folder "Nigeria".
      * Go to this folder and add "map" item from the "add item" drop-down
        menu.
      * If you go to the "map" you've created, you will notice that it
        can have an additional content type "overlay":
      * Choose "overlay" from "add item" drop-down menu
      * Enter Short Name and title of a new overlay
      * Click "browse" button for the "Markers Source" pop-up window to appear
      * Now choose the folder containing the object with the latitude-
        longitude parameters you want your marker to be tied to and click
        "insert"
      * Return to the "Edit Overlay" page to select the marker's color
        which will be shown on the map
      * Click the "Save" button
      * Complete the same steps for creating overlays for other objects of
        the folder "Nigeria"
      * Go to this folder and choose the map

Authors

  * Myroslav Opyr,   quintagroup.com

  * Vitaliy Podoba,  quintagroup.com
