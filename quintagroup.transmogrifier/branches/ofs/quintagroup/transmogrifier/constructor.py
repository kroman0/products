from zope.interface import classProvides, implements
from zope.component import queryUtility
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName

from quintagroup.transmogrifier.interfaces import IFTIConstructor4MetaType

class ConstructorSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)
    
    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.ttool = getToolByName(self.context, 'portal_types')
        
        self.typekey = defaultMatcher(options, 'type-key', name, 'type', 
                                      ('portal_type', 'Type'))
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.meta_types = filter(None, [i.strip() for i in
                                         options.get('meta-types', '').splitlines()])
    
    def __iter__(self):
        for item in self.previous:
            keys = item.keys()
            typekey = self.typekey(*keys)[0]
            pathkey = self.pathkey(*keys)[0]
            
            if not (typekey and pathkey):             # not enough info
                yield item; continue
            
            type_, path = item[typekey], item[pathkey]
            
            fti = self.ttool.getTypeInfo(type_)
            if fti is None:                           # not an existing type
                # Look for an IFTIConstructor4MetaType adapter
                mt = type_.startswith("meta_type:") and type_[10:] or None
                if mt in self.meta_types:
                    fti = queryUtility(IFTIConstructor4MetaType, name=mt)
                if fti is None:
                    yield item; continue

            elems = path.strip('/').rsplit('/', 1)
            container, id = (len(elems) == 1 and ('', elems[0]) or elems)
            context = self.context.unrestrictedTraverse(container, None)
            if context is None:                       # container doesn't exist
                yield item; continue

            if getattr(aq_base(context), id, None) is not None: # item exists
                yield item; continue

            obj = fti._constructInstance(context, id)
            obj = fti._finishConstruction(obj)
            if obj.getId() != id:
                item[pathkey] = '%s/%s' % (container, obj.getId())

            yield item
