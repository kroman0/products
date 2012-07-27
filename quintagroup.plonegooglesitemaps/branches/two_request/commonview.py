from zope.interface import implements, Interface, Attribute
from zope.component import queryMultiAdapter

from Acquisition import aq_inner, aq_parent
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

#from quintagroup.plonegooglesitemaps \
#    import qPloneGoogleSitemapsMessageFactory as _
from quintagroup.plonegooglesitemaps.interfaces import IBlackoutFilter
from quintagroup.plonegooglesitemaps.browser.utils import additionalURLs, \
     getUrlsObjects, urlFilter, OPERATIONS_PARSE 

from itertools import chain, starmap


SITEMAP_SIZE = 50000

class ISitemapView(Interface):
    """
    Sitemap view interface
    """

    def results():
        """ Return list of dictionary objects
            which confirm Sitemap conditions
        """

    def getAdditionalURLs():
        """ Return additional URL list
        """

    def updateRequest():
        """ Add compression header to RESPONSE
            if allowed
        """

    numEntries = Attribute("Return number of entries")


class CommonSitemapView(BrowserView):
    """
    Sitemap browser view
    """
    implements(ISitemapView)

    # key, function map for extend return results
    # with mapping data
    additional_maps = ()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def search_path(self):
        return '/'.join(aq_parent(aq_inner(self.context)).getPhysicalPath())

    def getFilteredObjects(self):
        """ Return brains
        """
        return []

    def defaultPagesInfo(self, func, url_filter=lambda x: x[0:x.rfind('/')]):
        """  Method gets default page. 
            It dedicated to generate {'http://...': func(brain),...}
        """
        objects = self.portal_catalog.searchResults(is_default_page=True)
        # func - this fuction gets info from brain
        # eg: func = lambda x: DateTime(x.ModificationDate)) 
        # url_filter - get parent object (url)
        return dict( 
                     (url_filter(url), func(brain))
               for 
                   url, brain 
               in 
                   getUrlsObjects(objects))

    def getObjectsInfo(self, modification_date):
        """ Gets info (list of tuples) for sitemap """
        # get all brains
        objects = self.getBOFiltered(self.getFilteredObjects())
        for url, brain in getUrlsObjects(objects):
            yield url, modification_date(brain), \
                  [(key, func(brain)) 
                       for 
                         key, func 
                       in 
                         self.additional_maps.iteritems()
                       if key != modification_date.__name__]
        
    def results(self):
        """ Prepare mapping for template
        """
        operations = [OPERATIONS_PARSE.match(op).groups() 
                      for op in self.context.getReg_exp()]

        # eg: additional_maps == {'modification_date': lambda x: xxx)}
        modification_date = self.additional_maps['modification_date']
        urls_info = self.defaultPagesInfo(modification_date)
        # after changing 'modification date' we'll change 
        # url according with filter
        num_entries = 0
        for url, date, additional_info in self.getObjectsInfo(modification_date):

            # TODO: check number of result. 
            # A Sitemap file can contain no more than 50,000 URLs.
            if num_entries > SITEMAP_SIZE:
               break 

            if url in urls_info:
                default_page_modification_date = urls_info.get(url) 

                # trying to update modification date
                date = date if date > default_page_modification_date \
                            else default_page_modification_date

            result = dict(additional_info)
            result.update({'modification_date': date.HTML4(),
                           'url': urlFilter(url, operations)})
            
            num_entries += 1
            yield result

    def getBOFiltered(self, objects):
        """Return black-out filtered objects
          Every record in blackout_list filter should follow the spec:
            [<filter name>:]<filter arguments>
          For example:
          1|  index.html
          2|  id:index.html
          3|  path:/folder_1_level/obj_in_folder
          4|  path:./folder_near_sitemap/obj_in_folder
          5|  foo_filter:arg-1, arg-2

          1->used default "id" filter - remove "index.html" objects;
          2->explicit "id" filter - remove "index.html" objects;
          3->"path" filter - remove /folder_1_level/obj_in_folder object,
              path from the root of the plone site;
          4->same to 3), but path get from the folder, where sitemap is
             located;
          5->filter name is "foo_filter" (must be registered IBlackoutFilter,
             named "foo_filter"), which get filter arguments: arg-1, arg-2

          Detailed explanation look in filters.txt doctest.
        """
        blackout_list = self.context.getBlackout_list()
        for frec in blackout_list:
            fspec = frec.split(":", 1)
            fargs = fspec.pop()
            fname = fspec and fspec.pop() or "id"
            fengine = queryMultiAdapter((self.context, self.request),
                          interface=IBlackoutFilter, name=fname)
            if fengine:
                objects = list(fengine.filterOut(objects, fargs))
        return objects

    def updateRequest(self):
        self.request.RESPONSE.setHeader('Content-Type', 'text/xml')
        try:
            compression = self.context.enableHTTPCompression()
            if compression:
                compression(request=self.request)
        except:
            pass

    def getAdditionalURLs(self):
        return additionalURLs(self.context)

    @property
    def numEntries(self):
        return len(self.results()) + len(self.getAdditionalURLs())
