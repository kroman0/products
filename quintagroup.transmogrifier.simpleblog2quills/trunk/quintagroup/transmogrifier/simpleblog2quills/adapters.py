import re
from xml.dom import minidom
from types import ListType
from types import TupleType

from zope.interface import implements, classProvides
from Products.CMFPlone.Portal import PloneSite
from Products.CMFCore import utils

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher

from quintagroup.transmogrifier.interfaces import IExportDataCorrector
from quintagroup.transmogrifier.adapters.exporting import ReferenceExporter
from quintagroup.transmogrifier.manifest import ManifestExporterSection

from quintagroup.transmogrifier.simpleblog2quills.interfaces import IExportItemManipulator, IBlog

IMAGE_FOLDER = 'images'

class BlogManifest(object):
    implements(IExportDataCorrector)

    def __init__(self, context):
        self.context = context

    def __call__(self, data):
        doc = data['data'].splitlines()
        record = '  <record type="Folder">%s</record>' % IMAGE_FOLDER
        doc = doc[:-1] + [record] + doc[-1:]
        data['data'] = '\n'.join(doc)
        return data

class BlogEntryManifest(object):
    implements(IExportItemManipulator)

    def __init__(self, context):
        self.context = context

    def __call__(self, item, **kw):
        # remove manifest data from item - content contained in BlogEntry isn't exported
        if '_files' in item and 'manifest' in item['_files']:
            del item['_files']['manifest']
        return item

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

    # HREF = re.compile(r'href="([^"]+)"')
    SRC = re.compile(r'src="([^"]+)"')

    # this shouldn't be there (store this for example as plone site property)
    SITE_URLS = [
        'http://4webresults.com/',
        'http://www.4webresults.com/'
    ]

    def __init__(self, context):
        self.context = context
        self.portal_url = utils.getToolByName(self.context, 'portal_url')
        self.portal = self.portal_url.getPortalObject()

    def __call__(self, data):
        data = super(BlogEntryExporter, self).__call__(data)
        doc = minidom.parseString(data['data'])
        try:
            elem = [i for i in doc.getElementsByTagName('field') if i.getAttribute('name') == 'body'][0]
        except IndexError:
            return data

        text = elem.firstChild.nodeValue
        urls = self.SRC.findall(text)
        blog = recurseToInterface(self.context, IBlog)
        blog_url = blog.absolute_url()
        blog_path = blog.getPhysicalPath()
        for url in urls:
            url = str(url)
            image_id = url.rsplit('/', 1)[-1]
            # bad link
            if '://' in url and not url.startswith('http://'):
                continue
            if url.startswith('http://'):
                for site in self.SITE_URLS:
                    if url.startswith(site):
                        # check whether image is stored in blog
                        relative_url = url[len(site):]
                        relative_url = relative_url.strip('/')
                        # if link is broken we'll get an AttributeError
                        try:
                            image = self.portal.unrestrictedTraverse(relative_url)
                        except AttributeError:
                            break
                        in_blog = recurseToInterface(image, IBlog) is not None and True or False
                        if in_blog:
                            new_url = '/'.join((blog_url, IMAGE_FOLDER, image_id))
                            text = text.replace(url, new_url, 1)
                        break
            else:
                if url.startswith('/'):
                    # if link is broken we'll get an AttributeError
                    try:
                        image = self.portal.unrestrictedTraverse(url.strip('/'))
                    except AttributeError:
                        continue
                else:
                    # if link is broken we'll get an AttributeError
                    try:
                        image = self.context.unrestrictedTraverse(url)
                    except AttributeError:
                        continue
                in_blog = recurseToInterface(image, IBlog) is not None and True or False
                if in_blog:
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
        item['_moved'] = True

        return item

class ImageFolderSection(object):
    """ This section will generate manifest files for image folders in blog.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.transmogrifier = transmogrifier

        self.flagkey = defaultMatcher(options, 'flag-key', name, 'moved')
        self.typekey = defaultMatcher(options, 'type-key', name, 'type')
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

    def __iter__(self):
        folders = {}

        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            typekey = self.typekey(*item.keys())[0]
            flagkey = self.flagkey(*item.keys())[0]

            # collect data about images moved to folders
            if pathkey and typekey and flagkey:
                path = item[pathkey]
                type_ = item[typekey]
                folder_path, image_id = path.rsplit('/', 1)
                folders.setdefault(folder_path, []).append((image_id, type_))

            yield item

        # generate manifests for those image folders
        items = []
        for folder, entries in folders.items():
            items.append({'_entries': entries, pathkey: folder})
        exporter = ManifestExporterSection(self.transmogrifier, 'manifest', {'blueprint': 'manifest'}, iter(items))
        for item in exporter:
            yield item
