qTopic 

The idea of qTopic is to allow building SmartFolder queries on custom catalogs 
added to Plone site. We had to update atct tool to keep the track of all catalogs 
indexes and metadata, cause standard implementation supports only portal_catalog.

Also we often had a need to return SmartFolder results in csv format, 
so simple one click exporter action was added.

qTopic itself is ATCTTopic extending class which allows to select catalog to be queried,
and has extra csv setup properties.

The atct monkey patch was tested with Plone tests, beside own test.

qTopic 0.1.3 is designed for Plone 2.0.5
qTopic 1.0 is for Plone 2.1.x and Plone 2.5



LICENSE
  
   see LICENSE.txt


INSTALATION
  
   install qTopic with quickinstaller in Plone


AUTHORS

   Volodymyr Cherepanyak, quintagroup.com.
   Mykola Harechko, quintagroup.com.