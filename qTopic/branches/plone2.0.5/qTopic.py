from locale import strcoll
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent, aq_inner

from Products.ATContentTypes.types.ATContentType import updateActions
from Products.ATContentTypes.types.ATTopic import ATTopic, IGNORED_FIELDS
from Products.ATContentTypes.interfaces.IATTopic import IATTopic
from Products.ATContentTypes.types.criteria import CriterionRegistry
from Products.ATContentTypes.Permissions import ChangeTopics, AddTopics
from Products.ATContentTypes.types.schemata import ATTopicSchema
from Products.ATContentTypes.interfaces.IATTopic import IATTopicSearchCriterion, IATTopicSortCriterion
from Products.Archetypes.public import *
from config import *

qTopic_schema = ATTopicSchema.copy() + Schema((
          StringField('catalog',
                       default = 'portal_catalog',
                       vocabulary = 'getCatalogList',
                       widget = SelectionWidget(label="Catalog",
                                       label_msgid="label_catalog",
                                       description="Select catalog to query",
                                       description_msgid="description_catalog")
          ),
          LinesField('exportFields',
                      vocabulary = 'getFieldsList',
                      schemata = 'export',
                      widget = MultiSelectionWidget(label="Fields to be exported",
                                           label_msgid="label_export_fields",
                                           description="Select fileds to be exported",
                                           description_msgid="description_export_fields")
          ),
          BooleanField('showHeader',
                      schemata = 'export',
                      default = 1,
                      widget = BooleanWidget(label="Print field headers",
                                             label_msgid="label_print_headers",
                                             description="Check if headers need to be printed",
                                             description_msgid="description_print_headers")
          ),
          StringField('delimiter',
                      default = ';',
                      schemata = 'export',
                      widget = StringWidget(label="Values delimiter",
                                            label_msgid="label_delimiter",
                                            description="Select delimiter to be used in CSV",
                                            description_msgid="description_delimiter",
                                            size = 4)
          ),
          ))


class qTopic(ATTopic):
    """A topic folder"""
    meta_type      = 'qTopic'
    portal_type    = 'qTopic'
    archetype_name = 'qTopic'
    typeDescription= ("qTopic is the same topic but with "+
                      "option of catlog selection")
    typeDescMsgId  = 'description_edit_topic'

    schema = qTopic_schema
    security       = ClassSecurityInfo()
    actions = updateActions(ATTopic,
        (
        {
        'id'          : 'export_csv',
        'name'        : 'Export in CSV',
        'action'      : 'string:${folder_url}/result_csv',
        'permissions' : (CMFCorePermissions.View,)
        },
       )
    )

    def getCatalogList(self):
        """ return list of catalog ids
        """
        at_tool = getToolByName(self, 'archetype_tool')
        catalogs = at_tool.getCatalogsInSite()
        return  DisplayList(zip(catalogs, catalogs))
   
    def getFieldsList(self):
        """ return DisplayList of fields
        """
        pcatalog = getToolByName( self, self.getCatalog() )
        available = pcatalog.schema()
        val = [ field
                 for field in available
                 if  field not in IGNORED_FIELDS
               ]
        val.sort(lambda x,y: strcoll(self.translate(x),self.translate( y)))
        return DisplayList(zip(val, val))

    security.declareProtected(ChangeTopics, 'criteriaByIndexId')
    def criteriaByIndexId(self, indexId):
        catalog_tool = getToolByName(self, self.getCatalog())
        indexObj = catalog_tool.Indexes[indexId]
        results = CriterionRegistry.criteriaByIndex(indexObj.meta_type)
        return results

    security.declareProtected(ChangeTopics, 'listFields')
    def listFields(self):
        """Return a list of fields from portal_catalog.
        """
        pcatalog = getToolByName( self, self.getCatalog() )
        available = pcatalog.indexes()
        val = [ field
                 for field in available
                 if  field not in IGNORED_FIELDS
               ]
        val.sort(lambda x,y: strcoll(self.translate(x),self.translate( y)))
        return val


    security.declareProtected(CMFCorePermissions.View, 'queryCatalog')
    def queryCatalog(self, REQUEST=None, **kw):
        """Invoke the catalog using our criteria to augment any passed
            in query before calling the catalog.
        """
        q = self.buildQuery()
        if q is None:
            # empty query - do not show anything
            return []
        kw.update(q)
        pcatalog = getToolByName(self, self.getCatalog())
        limit = self.getLimitNumber()
        max_items = self.getItemCount()
        if limit and self.hasSortCriterion():
            # Sort limit helps Zope 2.6.1+ to do a faster query
            # sorting when sort is involved
            # See: http://zope.org/Members/Caseman/ZCatalog_for_2.6.1
            kw.setdefault('sort_limit', max_items)
        results = pcatalog.searchResults(REQUEST, **kw)
        if limit:
            return results[:max_items]
        return results


registerType(qTopic, PROJECTNAME)

def modify_fti(fti):
    """Remove folderlisting action
    """
    actions = []
    for action in fti['actions']:
        if action['id'] == 'folderlisting':
                action['visible'] = False
                #actions.append(action)
    #fti['actions'] = tuple(actions)
