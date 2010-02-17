Introduction
============

This package intended for extend ZCatalog API with possiblity to
update selected columns only. This package register 'catalog_updater'
utility for that.

For simplify usage of the utility, it extend GenericSetup's ZCatalog
XMLAdapter handler, which allows *update* attribute usage in *column*
tag of *catalog.xml* file.

So, when you add new column to the catalog, you add catalog.xml file
in some profile with following part:

...
<column value="new_column" />
...

This add *new_column* metadata to the portal_catalog, BUT, this
metadata will be empty, untill you rebuild the catalog. For automate
this step - you can add 'update="True"' attribute to the tag. And this
lead to updte the column after adding. So result usage should be look
like:

...
<column value="new_column" update="True" />
...
