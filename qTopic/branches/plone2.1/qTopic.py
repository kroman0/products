from locale import strcoll
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent, aq_inner

from Products.ATContentTypes.content.base import updateActions
from Products.ATContentTypes.content.topic import ATTopic, IGNORED_FIELDS
from Products.ATContentTypes.interfaces import IATTopic
from Products.ATContentTypes.types.criteria import _criterionRegistry
from Products.ATContentTypes.permission import ChangeTopics, AddTopics
from Products.CMFCore.permissions import View
from Products.ATContentTypes.content.topic import ATTopicSchema
from Products.ATContentTypes.interfaces import IATTopicSearchCriterion, IATTopicSortCriterion
from Products.Archetypes.public import *
from config import *
from Products.CMFPlone.PloneBatch import Batch
from Products.ATContentTypes.config import TOOLNAME

qTopic_schema = ATTopicSchema.copy() + Schema((
          StringField("catalog",
                       default = "portal_catalog",
                       vocabulary = "getCatalogList",
                       widget = SelectionWidget(label="Catalog",
                                       label_msgid="label_catalog",
                                       description="Select catalog to query",
                                       description_msgid="description_catalog")
          ),
          BooleanField("showHeader",
                      schemata = "export",
                      default = 1,
                      widget = BooleanWidget(label="Print field headers",
                                             label_msgid="label_print_headers",
                                             description="Check if headers need to be printed",
                                             description_msgid="description_print_headers")
          ),
          StringField("delimiter",
                      default = ";",
                      schemata = "export",
                      widget = StringWidget(label="Values delimiter",
                                            label_msgid="label_delimiter",
                                            description="Select delimiter to be used in CSV",
                                            description_msgid="description_delimiter",
                                            size = 4)
          ),
          ))
qTopic_schema["customViewFields"].schemata = "export"
qTopic_schema["customViewFields"].vocabulary = "getFieldsList"
qTopic_schema["customViewFields"].default=("id","getFullName","getEmail")

class qTopic(ATTopic):
    """A topic folder"""
    meta_type      = "qTopic"
    portal_type    = "qTopic"
    archetype_name = "qTopic"
    typeDescription= ("qTopic is the same topic but with "+
                      "option of catlog selection")
    typeDescMsgId  = "description_edit_topic"

    schema = qTopic_schema
    security       = ClassSecurityInfo()
    actions = updateActions(ATTopic,
        (
        {
        "id"          : "export_csv",
        "name"        : "Export in CSV",
        "action"      : "string:${folder_url}/result_csv",
        "permissions" : (CMFCorePermissions.View,)
        },
       )
    )

    def getCatalogList(self):
        """ return list of catalog ids
        """
        at_tool = getToolByName(self, "archetype_tool")
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
        return [(i, i, i)for i in val]

    security.declareProtected(ChangeTopics, "criteriaByIndexId")
    def criteriaByIndexId(self, indexId):
        """ get createrias bu index """
        catalog_tool = getToolByName(self, self.getCatalog())
        indexObj = catalog_tool.Indexes[indexId]
        results = _criterionRegistry.criteriaByIndex(indexObj.meta_type)
        return results

    security.declareProtected(View, 'allowedCriteriaForField')
    def allowedCriteriaForField(self, field, display_list=False):
        """ Return all valid criteria for a given field.  Optionally include
            descriptions in list in format [(desc1, val1) , (desc2, val2)] for
            javascript selector."""
        tool = getToolByName(self, self.getCatalog())
        criteria = _criterionRegistry.listTypes()
        allowed = [crit for crit in criteria
                                if crit in self.criteriaByIndexId(field)]
        if display_list:
            flat = []
            for a in allowed:
                desc = _criterionRegistry[a].shortDesc
                flat.append((a,desc))
            allowed = DisplayList(flat)
        return allowed
    """
    security.declareProtected(ChangeTopics, "listFields")
    def listFields(self):
        pcatalog = getToolByName( self, self.getCatalog() )
        available = pcatalog.indexes()
        val = [ field
                 for field in available
                 if  field not in IGNORED_FIELDS
               ]
        val.sort(lambda x,y: strcoll(self.translate(x),self.translate( y)))
        return [(i, i, i)for i in val]
     """
    security.declareProtected(ChangeTopics, "listFields")
    def listFields(self):
        """Return a list of fields from portal_catalog.
        """
        tool = getToolByName(self, TOOLNAME)
        return tool.getEnabledFields(catalog_name=self.getCatalog())

    security.declareProtected(ChangeTopics, 'listAvailableFields')
    def listAvailableFields(self):
        """Return a list of available fields for new criteria.
        """
        return self.listFields()
    
    security.declareProtected(View, 'listMetaDataFields')
    def listMetaDataFields(self, exclude=True):
        """Return a list of metadata fields from portal_catalog.
        """
        tool = getToolByName(self, TOOLNAME)
        catalog_name=self.getCatalog()
        return tool.getMetadataDisplay(exclude,catalog_name=catalog_name)

    security.declareProtected(CMFCorePermissions.View, "queryCatalog")
    def queryCatalog(self, REQUEST=None, batch=False, b_size=None,
                                                    full_objects=False, **kw):
        """Invoke the catalog using our criteria to augment any passed
            in query before calling the catalog.
        """
        if REQUEST is None:
            REQUEST = getattr(self, 'REQUEST', {})
        b_start = REQUEST.get('b_start', 0)

        q = self.buildQuery()
        if q is None:
            # empty query - do not show anything
            if batch:
                return Batch([], 20, int(b_start), orphan=0)
            return []
        # Allow parameters to further limit existing criterias
        for k,v in q.items():
            if kw.has_key(k):
                arg = kw.get(k)
                if isinstance(arg, (ListType,TupleType)) and isinstance(v, (ListType,TupleType)):
                    kw[k] = [x for x in arg if x in v]
                elif isinstance(arg, StringType) and isinstance(v, (ListType,TupleType)) and arg in v:
                    kw[k] = [arg]
                else:
                    kw[k]=v
            else:
                kw[k]=v
        #kw.update(q)
        pcatalog = getToolByName(self, self.getCatalog())
        limit = self.getLimitNumber()
        max_items = self.getItemCount()
        # Batch based on limit size if b_szie is unspecified
        if max_items and b_size is None:
            b_size = int(max_items)
        else:
            b_size = 20
        if limit and max_items and self.hasSortCriterion():
            # Sort limit helps Zope 2.6.1+ to do a faster query
            # sorting when sort is involved
            # See: http://zope.org/Members/Caseman/ZCatalog_for_2.6.1
            kw.setdefault('sort_limit', max_items)
        __traceback_info__ = (self, kw,)
        results = pcatalog.searchResults(REQUEST, **kw)
        if full_objects and not limit:
            results = [b.getObject() for b in results]
        if batch:
            batch = Batch(results, b_size, int(b_start), orphan=0)
            return batch
        if limit:
            if full_objects:
                return [b.getObject() for b in results[:max_items]]
            return results[:max_items]
        return results



registerType(qTopic, PROJECTNAME)

def modify_fti(fti):
    """Remove folderlisting action
    """
    actions = []
    for action in fti["actions"]:
        if action["id"] == "folderlisting":
                action["visible"] = False
                #actions.append(action)
    #fti["actions"] = tuple(actions)
