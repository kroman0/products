from plone.indexer import indexer
from plone.app.layout.navigation.defaultpage import getDefaultPage

from zope.interface import Interface

from quintagroup.plonegooglesitemaps.utils import dateTime


@indexer(Interface)
def sitemap_date(obj):
    """ Method gets date for sitemap """

    def lastModificationDate(folderish_date, default_page):
        """  Method compares date (folderish object)
            with another date (default_page) and returns the last
        """

        # get modification date
        child_mdate = dateTime(default_page)
        last_date = folderish_date if folderish_date > child_mdate \
                                else child_mdate

        child = getDefaultPage(default_page)
        if not child:
            return last_date

        return lastModificationDate(last_date,
                                    default_page[child])

    default_page = getDefaultPage(obj)
    # get modification date
    date = dateTime(obj)
    if default_page:
        date = lastModificationDate(date, getattr(obj, default_page))

    return date.HTML4()
