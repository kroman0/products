import re
from xml.dom import minidom
from types import ListType
from types import TupleType

from zope.interface import implements, classProvides
from zope.app.annotation.interfaces import IAnnotations

from Products.CMFPlone.Portal import PloneSite
from Products.CMFCore import utils

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher

from quintagroup.transmogrifier.interfaces import IExportDataCorrector, IImportDataCorrector
from quintagroup.transmogrifier.adapters.exporting import ReferenceExporter
from quintagroup.transmogrifier.manifest import ManifestExporterSection
from quintagroup.transmogrifier.logger import VALIDATIONKEY

from quintagroup.transmogrifier.simpleblog2quills.interfaces import IExportItemManipulator, IBlog

# URL of the site, where blog is located (this is needed to fix links in entries)
SITE_URLS = []
IMAGE_FOLDER = 'images'
# this registries are needed to avoid loosing images with equal ids
IMAGE_IDS = []
IMAGE_PATHS = {}

class BlogManifest(object):
    implements(IExportDataCorrector)

    def __init__(self, context):
        self.context = context

    def __call__(self, data):
        doc = minidom.parseString(data['data'])
        root = doc.documentElement
        for child in root.getElementsByTagName('record'):
            if child.getAttribute('type') not in  ('BlogEntry', 'BlogFolder'):
                root.removeChild(child)
        folder = doc.createElement('record')
        folder.setAttribute('type', 'Large Plone Folder')
        folder.appendChild(doc.createTextNode(IMAGE_FOLDER))
        root.appendChild(folder)
        data['data'] = doc.toxml('utf-8')
        return data

class BlogFolderManifest(object):
    implements(IExportDataCorrector)

    def __init__(self, context):
        self.context = context

    def __call__(self, data):
        doc = minidom.parseString(data['data'])
        root = doc.documentElement
        for child in root.getElementsByTagName('record'):
            if child.getAttribute('type') not in  ('BlogEntry', 'BlogFolder'):
                root.removeChild(child)
        data['data'] = doc.toxml('utf-8')
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

def getUniqueId(image_id):
    """ Generate id that is unique in IMAGE_IDS registry.
    """
    if '.' in image_id:
        name, ext = image_id.rsplit('.', 1)
        ext = '.' + ext
    else:
        name, ext = image_id, ''
    if image_id in IMAGE_IDS:
        c = 1
        new_id = name + str(c) + ext
        while new_id in IMAGE_IDS:
            c += 1
            new_id = name + str(c) + ext
        image_id = new_id

    return image_id

class BlogEntryExporter(ReferenceExporter):
    implements(IExportDataCorrector)

    SRC = re.compile(r'src="([^"]+)"')

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
        blog_path = blog.getPhysicalPath()
        context_path = self.context.getPhysicalPath()
        for url in urls:
            url = str(url)
            image_id = url.rsplit('/', 1)[-1]
            # skip links with illegal url schema
            if '://' in url and not url.startswith('http://'):
                continue
            # convert all all links to relative
            if url.startswith('http://'):
                for site in SITE_URLS:
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
                            image_id = self.fixImageId(image, image_id, blog_path)
                            level = len(context_path) - len(blog_path) - 1
                            new_url = '/'.join(['..' for i in range(level)])
                            new_url = '/'.join((new_url, IMAGE_FOLDER, image_id))
                            text = text.replace(url, new_url, 1)
                        else:
                            # find how many levels self.context is under portal root
                            level = len(context_path) - 3
                            new_url = '/'.join(['..' for i in range(level)])
                            new_url  = new_url + '/' + relative_url
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
                    image_id = self.fixImageId(image, image_id, blog_path)
                    level = len(context_path) - len(blog_path) - 1
                    new_url = '/'.join(['..' for i in range(level)])
                    new_url = '/'.join([new_url, IMAGE_FOLDER, image_id])
                    text = text.replace(url, new_url, 1)
                elif url.startswith('../'):
                    # remove '../' from the start of string
                    new_url = url[3:]
                    text = text.replace(url, new_url, 1)
                elif url.startswith('/'):
                    # these links didn't work so rewrite them with '..'
                    # find how many levels self.context is under portal root
                    level = len(context_path) - 3
                    new_url = '/'.join(['..' for i in range(level)])
                    new_url  = new_url + url
                    text = text.replace(url, new_url, 1)

        elem.firstChild.nodeValue = text
        data['data'] = doc.toxml('utf-8')
        return data

    def fixImageId(self, image, image_id, blog_path):
        """ Check whether image is good or generate new if it's bad.
        """
        image_path = '/'.join(image.getPhysicalPath())
        if image_id in IMAGE_IDS and image_path not in IMAGE_PATHS:
            image_id = getUniqueId(image_id)
        if image_id not in IMAGE_IDS:
            IMAGE_IDS.append(image_id)
            IMAGE_PATHS[image_path] = '/'.join(blog_path[2:] + (IMAGE_FOLDER, image_id))

        return image_id

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

        blog_path = blog.getPhysicalPath()
        full_path = '/'.join(self.context.getPhysicalPath())
        image_id = path.rsplit('/', 1)[-1]
        modified = False

        if full_path in IMAGE_PATHS:
            new_path = IMAGE_PATHS[full_path]
        else:
            unique_id = getUniqueId(image_id)
            modified = image_id != unique_id
            new_path = '/'.join(blog_path[2:] + (IMAGE_FOLDER, unique_id))

            IMAGE_IDS.append(image_id)
            IMAGE_PATHS[full_path] = new_path

        # change item's path
        item[pathkey] = new_path
        item['_oldpath'] = path

        # now we need to fix object id in .marshall.xml
        if modified:
            if '_files' in item and 'marshall' in item['_files']:
                doc = minidom.parseString(item['_files']['marshall']['data'])
                elem = [i for i in doc.getElementsByTagName('field') if i.getAttribute('name') == 'id'][0]
                elem.firstChild.nodeValue = '\n\t\t%s\n\t' % unique_id
                item['_files']['marshall']['data'] = doc.toxml('utf-8')

        return item

class ImageFolderSection(object):
    """ This section will generate manifest files for image folders in blog.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.transmogrifier = transmogrifier

        self.flagkey = defaultMatcher(options, 'old-path-key', name, 'oldpath')
        self.typekey = defaultMatcher(options, 'type-key', name, 'type')
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')


        site_urls = options.get('site-urls', '')
        site_urls = filter(None, [i.strip() for i in site_urls.splitlines()])
        for i in site_urls:
            SITE_URLS.append(i)

        self.anno = IAnnotations(transmogrifier)

    def __iter__(self):
        folders = {}

        # safely get logging storage
        if VALIDATIONKEY in self.anno:
            log_storage = self.anno[VALIDATIONKEY]
        else:
            log_storage = None

        for item in self.previous:
            item_keys = item.keys()
            pathkey = self.pathkey(*item_keys)[0]
            typekey = self.typekey(*item_keys)[0]
            oldpathkey = self.flagkey(*item_keys)[0]

            # collect data about images moved to folders
            if pathkey and typekey and oldpathkey:
                path = item[pathkey]
                old_path = item[oldpathkey]
                type_ = item[typekey]
                folder_path, image_id = path.rsplit('/', 1)
                folders.setdefault(folder_path, []).append((image_id, type_))

                # update logging data (path) for this item
                if log_storage and log_storage[-1] == old_path:
                    log_storage.pop()
                    log_storage.append(path)

            yield item

        # generate manifests for those image folders
        items = []
        for folder, entries in folders.items():
            items.append({'_entries': entries, pathkey: folder})
        exporter = ManifestExporterSection(self.transmogrifier, 'manifest', {'blueprint': 'manifest'}, iter(items))
        for item in exporter:
            yield item

        # clean registries
        while IMAGE_IDS: IMAGE_IDS.pop()
        while SITE_URLS: SITE_URLS.pop()
        IMAGE_PATHS.clear()

class WorkflowImporter(object):
    """ This adapter tries to convert all possible workflow histories to 
        simple_publication_workflow history.
    """
    implements(IImportDataCorrector)

    def __init__(self, context):
        self.context = context

    def __call__(self, data):
        doc = minidom.parseString(data['data'])
        wh = [i for i in doc.getElementsByTagName('cmf:workflow')]
        if not wh:
            # we don't have such workflow history
            return data

        wh = wh[0]
        workflow_id = wh.getAttribute('id')
        if workflow_id == 'simple_publication_workflow':
            return data
        wh.setAttribute('id', 'simple_publication_workflow')
        if workflow_id == 'simpleblog_workflow':
            self.fixSimpleBlogWorkflow(wh)
        else:
            self.fixWorkflow(wh)

        data['data'] = doc.toxml('utf-8')
        return data

    def fixSimpleBlogWorkflow(self, wh):
        for history in wh.getElementsByTagName('cmf:history'):
            for var in history.getElementsByTagName('cmf:var'):
                id_ = var.getAttribute('id')
                value = var.getAttribute('value')
                if id_ == 'review_state' and value == 'draft':
                    var.setAttribute('value', 'private')

    def fixWorkflow(self, wh):
        for history in wh.getElementsByTagName('cmf:history'):
            for var in history.getElementsByTagName('cmf:var'):
                id_ = var.getAttribute('id')
                value = var.getAttribute('value')
                if id_ == 'review_state' and value == 'visible':
                    var.setAttribute('value', 'published')
