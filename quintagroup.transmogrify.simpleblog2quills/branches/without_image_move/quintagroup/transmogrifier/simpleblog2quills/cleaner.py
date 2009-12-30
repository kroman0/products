import logging
from zope.interface import classProvides, implements

from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection

from zExceptions import BadRequest
from Acquisition import aq_inner, aq_parent, aq_base
from Products.CMFCore import utils

log = logging.getLogger('quintagroup.transmogrifier.simpleblog2quills.blogentrycleaner')

class BlogEntryCleaner(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.context = transmogrifier.context
        self.previous = previous

    def __iter__(self):
        for entry in self.getNotEmptyEntries():
            self.moveContainedUp(entry)

        for item in self.previous:
            yield item

    def moveContainedUp(self, entry):
        """ Move contained object from blog entry one level up.
        """
        entry = aq_inner(entry)
        ids = entry.contentIds()
        parent = aq_parent(entry)
        try:
            parent.manage_pasteObjects(entry.manage_cutObjects(ids))
            log.info('Moving from %s BlogEntry next objects: %s' % ('/'.join(entry.getPhysicalPath()), ids))
        except Exception, e:
            log.error('Failed to move from %s BlogEntry next objects: %s\n%s' % ('/'.join(entry.getPhysicalPath()), ids, e))

    def getNotEmptyEntries(self):
        """ Find all blog entries in the site that have contained objects.
        """
        not_empty = []
        catalog = utils.getToolByName(self.context, 'portal_catalog')
        for entry in catalog(portal_type='BlogEntry'):
            entry = entry.getObject()
            contained = entry.contentIds()
            if contained:
                not_empty.append(entry)
        return not_empty
