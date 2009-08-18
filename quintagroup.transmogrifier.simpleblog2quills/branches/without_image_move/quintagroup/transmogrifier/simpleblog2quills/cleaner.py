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

        log.info('Moving from %s BlogEntry next objects: %s' % ('/'.join(entry.getPhysicalPath()), ids))
        for obj_id in ids:
            obj = entry._getOb(obj_id)
            entry._delObject(obj_id, suppress_events=True)
            obj = aq_base(obj)
            new_id = self.generateId(parent, obj_id)
            if new_id != obj_id:
                log.info('Changing id from %s to %s' % (obj_id, new_id))
                obj._setId(new_id)
            try:
                parent._setObject(new_id, obj, set_owner=0, suppress_events=True)
            except BadRequest, e:
                log.error(e)

    def generateId(self, folder, id_):
        c = 1
        existing = folder.objectIds()
        new_id = id_
        while True:
            if id_ in existing:
                id_ = new_id + str(c)
                c += 1
            else:
                return new_id

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
