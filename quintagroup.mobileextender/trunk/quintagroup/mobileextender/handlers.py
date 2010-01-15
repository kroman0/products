from zope.interface import alsoProvides, providedBy
from interfaces import IMobile

def markAsMobile(object, event):
    mobfield = object.Schema().get('mobile_content',None)
    if mobfield and mobfield.get(object):
        if not IMobile in providedBy(object):
            alsoProvides(object, IMobile)
            object.reindexObject(idxs=['object_provides'])
