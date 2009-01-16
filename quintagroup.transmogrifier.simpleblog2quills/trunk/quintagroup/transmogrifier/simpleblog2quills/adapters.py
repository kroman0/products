import re
from xml.dom import minidom
from types import ListType
from types import TupleType

from zope.interface import implements
from Products.CMFPlone.Portal import PloneSite

from quintagroup.transmogrifier.interfaces import IExportDataCorrector
from quintagroup.transmogrifier.adapters.exporting import ReferenceExporter

from quintagroup.transmogrifier.simpleblog2quills.interfaces import IExportItemManipulator, IBlog

IMAGE_FOLDER = 'images'

class BlogExporter(object):
    implements(IExportDataCorrector)

    def __init__(self, context):
        self.context = context

    def __call__(self, data):
        return data

def recurseToInterface(item, ifaces):
    """Recurse up the aq_chain until an object providing `iface' is found,
    and return that.
    """
    if not isinstance(ifaces, (ListType, TupleType)):
        ifaces = [ifaces]
    parent = item.aq_parent
    for iface in ifaces:
        if iface.providedBy(item):
            return item
    for iface in ifaces:
        if iface.providedBy(parent):
            return parent
    if isinstance(parent, PloneSite):
        # Stop when we get to the portal root.
        return None
    return recurseToInterface(parent, ifaces)

class BlogEntryExporter(ReferenceExporter):
    implements(IExportDataCorrector)

    HREF = re.compile(r'href="([^"]+)"')
    SRC = re.compile(r'src="([^"]+)"')

    def __call__(self, data):
        data = super(BlogEntryExporter, self)(data)
        doc = minidom.parseString(data['data'])
        try:
            elem = [i for i in doc.getElementsByTagName('field') if i.getAttribute('name') == 'body'][0]
        except IndexError:
            return data

        text = elem.firstChild.nodeValue
        # urls = self.HREF.findall(text)
        urls = self.SRC.findall(text)
        blog = recurseToInterface(self.context, IBlog)
        blog_url = blog.absolute_url()
        blog_path = blog.getPhysicalPath()
        for url in urls:
            image_id = url.rsplit('/', 1)[-1]
            if url.startswith('http://'):
                new_url = '/'.join((blog_url, IMAGE_FOLDER, image_id))
            else:
                path = self.context.getPhysicalPath()
                # /plone/blog 2
                # /plone/blog/bloggins/entry 4
                # ../../images
                level = len(path) - len(blog_path)
                new_url = '/'.join(['..' for i in range(level)])
                new_url = '/'.join([new_url, IMAGE_FOLDER, image_id])

            text = text.replace(url, new_url, 1)

        elem.firstChild.nodeValue = text
        data['data'] = doc.toxml('utf-8')
        return data

class PathRewriter(object):
    implements(IExportItemManipulator)

    def __init__(self, context):
        self.context = context

    def __call__(self, item, **kw):
        pathkey = kw.get('path')
        if pathkey is None:
            return item

        path = item[pathkey]
        blog = recurseToInterface(self.context, IBlog)
        if blog is None:
            return item

        new_path = list(blog.getPhysicalPath())[2:]
        new_path.append(IMAGE_FOLDER)
        new_path.append(self.context.getId())
        new_path = '/'.join(new_path)
        item[pathkey] = new_path

        return item
