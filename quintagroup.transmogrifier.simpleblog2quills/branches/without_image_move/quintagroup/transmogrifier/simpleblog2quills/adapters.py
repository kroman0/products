import re
from xml.dom import minidom

from zope.interface import implements

from Products.CMFCore import utils

from quintagroup.transmogrifier.interfaces import IExportDataCorrector, IImportDataCorrector
from quintagroup.transmogrifier.adapters.exporting import ReferenceExporter

from quintagroup.transmogrifier.simpleblog2quills.interfaces import IExportItemManipulator

class BlogEntryManifest(object):
    implements(IExportItemManipulator)

    def __init__(self, context):
        self.context = context

    def __call__(self, item, **kw):
        # remove manifest data from item - content contained in BlogEntry isn't exported
        if '_files' in item and 'manifest' in item['_files']:
            del item['_files']['manifest']
        return item

class BlogEntryExporter(ReferenceExporter):
    implements(IExportDataCorrector)

    SRC = re.compile(r'src="([^"]+)"')

    def __init__(self, context):
        self.context = context
        self.portal_url = utils.getToolByName(self.context, 'portal_url')
        self.portal = self.portal_url.getPortalObject()

        # try to get site domain (maybe it's stored 
        # in portal_properties/site_properties/title property)
        self.site_domains = []
        portal_properties = utils.getToolByName(self.context, 'portal_properties')
        domain = portal_properties.site_properties.getProperty('title')
        if domain is not None:
            if domain.startswith('www.'):
                self.site_domains.append(domain)
            else:
                self.site_domains.append(domain)
                self.site_domains.append('www.' + domain)

    def __call__(self, data):
        data = super(BlogEntryExporter, self).__call__(data)
        doc = minidom.parseString(data['data'])
        try:
            elem = [i for i in doc.getElementsByTagName('field') if i.getAttribute('name') == 'body'][0]
        except IndexError:
            return data

        text = elem.firstChild.nodeValue
        urls = self.SRC.findall(text)
        context_path = self.context.getPhysicalPath()

        # convert all links to relative and 
        # make them work without virtual hosting
        for url in urls:
            url = str(url)
            # skip links with illegal url schema
            if '://' in url and not url.startswith('http://'):
                continue
            if url.startswith('http://'):
                for domain in self.site_domains:
                    if url.startswith(domain):
                        # check whether image is stored in blog
                        relative_url = url[len(domain):]
                        relative_url = relative_url.strip('/')
                        # if link is broken we'll get an AttributeError
                        try:
                            image = self.portal.unrestrictedTraverse(relative_url)
                        except AttributeError:
                            break
                        level = len(context_path) - 3
                        new_url = '/'.join(['..' for i in range(level)])
                        new_url  = new_url + '/' + relative_url
                        text = text.replace(url, new_url, 1)
                        break
            else:
                # if link is broken we'll get an AttributeError
                if url.startswith('/'):
                    try:
                        image = self.portal.unrestrictedTraverse(url.strip('/'))
                    except AttributeError:
                        continue
                else:
                    try:
                        image = self.context.unrestrictedTraverse(url)
                    except AttributeError:
                        continue

                if url.startswith('../'):
                    # BlogEntry is folderish object and links to images that
                    # are is the same folder as BlogEntry starts with '..'
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
