from zope.interface import classProvides, implements
from zope import event

from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher

from Products.CMFCore import utils
from Products.CMFCore.WorkflowCore import WorkflowException

try:
    from zope.interface import alsoProvides
    from quills.core.interfaces.enabled import IWeblogEnhanced, IPossibleWeblog
    from Products.QuillsEnabled.activation import WeblogActivationEvent
except ImportError:
    # this try: ... except: ... clause is needed for this package to work on 
    # plone 2.1, because zcml:condition attribute in zcml doesn't work
    pass

from quintagroup.transmogrifier.simpleblog2quills.adapters import IMAGE_FOLDER

class BlogActivatorSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.context = transmogrifier.context
        self.wftool = utils.getToolByName(self.context, 'portal_workflow')

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.flagkey = options.get('flag-key', '_old_type').strip()
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]

            if not pathkey:
                yield item; continue

            type_ = item.get(self.flagkey, None)
            newtype = item.get('_type', None)
            if type_ != 'Blog' and newtype != 'Large Plone Folder':
                yield item; continue

            path = item[pathkey]
            if type_ is None and newtype == 'Large Plone Folder':
                parts = path.rsplit('/', 1)
                if len(parts) == 2:
                    parent, id_ = parts
                else:
                    yield item; continue
                if id_ != IMAGE_FOLDER:
                    yield item; continue

            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:         # path doesn't exist
                yield item; continue

            if type_ == 'Blog' and newtype == 'Large Plone Folder':
                # mark as blog
                if not IWeblogEnhanced.providedBy(obj) and \
                    IPossibleWeblog.providedBy(obj):
                    alsoProvides(obj, IWeblogEnhanced)
                    event.notify(WeblogActivationEvent(obj))
            elif type_ is None and newtype == 'Large Plone Folder':
                # pulish 'images' subfolder
                parent = self.context.unrestrictedTraverse(parent, None)
                if IWeblogEnhanced.providedBy(parent) :
                    try:
                        self.wftool.doActionFor(obj, 'publish')
                    except WorkflowException:
                        pass

            yield item

        # reindex provided interfaces
        catalog = utils.getToolByName(self.context, 'portal_catalog')
        catalog.reindexIndex('object_provides', None)
