from zope.schema.vocabulary import SimpleVocabulary

from Products.PluginIndexes.FieldIndex import FieldIndex
from Products.PluginIndexes.KeywordIndex import KeywordIndex
from Products.PluginIndexes.DateIndex import DateIndex
from Products.PluginIndexes.DateRangeIndex import DateRangeIndex
from Products.CMFCore.utils import getToolByName

SORT_INDICES = (FieldIndex, KeywordIndex, DateIndex, DateRangeIndex)
#SORT_INDICES = ('DateIndex', 'DateRangeIndex', 'FieldIndex', 'KeywordIndex')
def getSortIndices( context ):
    catalog = getToolByName(context, 'portal_catalog')
    return SimpleVocabulary.fromValues(
        [k for k,v in catalog._catalog.indexes.items() if type(v) in SORT_INDICES])

def getPortalTypes( context ):
    pt = getToolByName(context, 'portal_types')
    return SimpleVocabulary.fromValues(pt.listContentTypes())


def getPortalPath( context ):
    return getToolByName(context, 'portal_url').getPortalPath()

def getWFStates( context ):
    pwf = getToolByName(context, 'portal_workflow')
    utokens = {}
    [utokens.update({k:v}) for k,v in pwf.listWFStatesByTitle() if k not in utokens.keys()]
    return SimpleVocabulary.fromItems(utokens.items())


