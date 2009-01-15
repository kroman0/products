from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish
from Products.Archetypes.interfaces import IBaseFolder

ALLWAYS_EXISTING_ATTRIBUTES = ('index_html', )

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
                yield item; continue
            
            elems = path.strip('/').rsplit('/', 1)
            container, id = (len(elems) == 1 and ('', elems[0]) or elems)
            context = self.context.unrestrictedTraverse(container, None)
            if context is None:                       # container doesn't exist
                yield item; continue
            
            # check if context is container, if we didn't do this AttributeError
            # will be raised when calling fti._constructInstance(context, id)
            if not (IFolderish.providedBy(context) or IBaseFolder.providedBy(context)):
                # we can't construct this content item, so remove it from pipeline
                continue
            
            # content object always have some default attributes, but sometimes
            # these attributes can be also used as content ids
            if id in ALLWAYS_EXISTING_ATTRIBUTES:
                o = getattr(aq_base(context), id)
                # check if it is content object (is instance of some portal type)
                if getattr(aq_base(o), 'getPortalTypeName', None) is not None:
                    yield item; continue
            elif getattr(aq_base(context), id, None) is not None: # item exists
                yield item; continue
            
            obj = fti._constructInstance(context, id)
            obj = fti._finishConstruction(obj)
            if obj.getId() != id:
                item[pathkey] = '%s/%s' % (container, obj.getId())
            
            yield item
