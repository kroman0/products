from zope.interface import classProvides, implements
from zope import event

from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher

try:
    from zope.interface import alsoProvides
    from quills.core.interfaces.enabled import IWeblogEnhanced, IPossibleWeblog
    from Products.QuillsEnabled.activation import WeblogActivationEvent
except ImportError:
    # this try: ... except: ... clause is needed for this package to work on 
    # plone 2.1, because zcml:condition attribute in zcml doesn't work
    pass

class BlogActivatorSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.context = transmogrifier.context

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.flagkey = options.get('flag-key', '_old_type').strip()
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]

            if not pathkey or self.flagkey not in item:
                yield item; continue

            if item[self.flagkey] != 'Blog':
                yield item; continue

            path = item[pathkey]
            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:         # path doesn't exist
                yield item; continue

            if not IWeblogEnhanced.providedBy(obj) and \
                IPossibleWeblog.providedBy(obj):
                alsoProvides(obj, IWeblogEnhanced)
                event.notify(WeblogActivationEvent(obj))

            yield item
