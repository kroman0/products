quintagroup.canonicalpath Package Readme
========================================

The package serves for possibility to define path and/or link for the
object, which may differ from standard Physical path or URL in portal.
It's uses by such products as quintagroup.seoptimizer (for defining
canonical link of the object), quintagroup.plonegooglesitemaps (on
google sitemaps generation).

This package intended for bring *canonical_path* and/or
*canonical_link* property to any traversable object. For that it
defines ICanonicalPath and ICanonicalLink interfaces, and register
basic adapters for ITraversable objects.

Also package register *canonical_path* and *canonical_link* indexers
for possible usage in catalog (ZCatalog).

Default adapters behaviour:

  - *canonical_path* return path from portal root, i.e. for
    `/plone/front-page` *canonical_path* will be `/front-page`.
  - *canonical_link* return absoulute url of the object.
