from Products.CMFCore.utils import getToolByName

from Products.GenericSetup.interfaces import IFilesystemImporter
from zope.component import queryAdapter

def importPASContent(context):
    acl_us = getToolByName(context.getSite(), 'acl_users')
    IFilesystemImporter(acl_us).import_(context, 'PAS', True)