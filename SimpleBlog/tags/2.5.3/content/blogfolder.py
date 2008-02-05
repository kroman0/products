from Products.Archetypes.public import BaseFolderSchema, Schema
from Products.Archetypes.public import StringField, LinesField, ComputedField, ComputedWidget
from Products.Archetypes.public import LinesWidget, TextAreaWidget, IdWidget, StringWidget
from Products.Archetypes.public import BaseFolder, registerType
from Products.CMFCore import CMFCorePermissions

from Products.ATContentTypes.content.base import  ATCTBTreeFolder, ATCTFolder
from Products.ATContentTypes.lib.constraintypes import  ConstrainTypesMixinSchema

import Products.SimpleBlog.Permissions


schema = ConstrainTypesMixinSchema.copy() + ATCTFolder.schema.copy() +  Schema((
    StringField('description',
                isMetadata=1,
                accessor='Description',
                widget=TextAreaWidget(label='Description', 
                                      label_msgid="label_blogfolder_description",
                                      description_msgid="help_blogfolder_description",
                                      i18n_domain="SimpleBlog",
                                      description='Give a description for this SimpleBlog folder.'),),
    ComputedField('existingCats', 
                  expression='here.getInheritedCategories()',
                  widget=ComputedWidget(label='Existing categories.', 
                                  label_msgid="label_blogfolder_existing_cats",
                                  i18n_domain="SimpleBlog",)),
    LinesField('categories', 
               widget=LinesWidget(label='Additional categories', 
                                  label_msgid="label_additional_categories",
                                  description_msgid="help_additional_categories",
                                  i18n_domain="SimpleBlog",
                                  description='Supply a list of possible additional categories that will be available to BlogEntries inside this folder or in sub folders.'),
               )
        ))


class BlogFolder(ATCTBTreeFolder, ATCTFolder):
    """
    A folder object to store BlogEntries in
    """
    portal_type = meta_type = 'BlogFolder'
    archetype_name = 'Blog Folder'
    content_icon='blogfolder_icon.gif'
    schema = schema
    global_allow=0
    
    default_view = 'simpleblog_view_title_description'
    immediate_view = 'simpleblog_view_title_description'
    suppl_views = ('simpleblog_view_title_description', 'simpleblog_view_title', 'simpleblog_view_title_description_body',  'folder_listing')

    filter_content_types=1    
    
    allowed_content_types=('BlogEntry', 'BlogFolder', 'Link', 'Image', 'File', 'Portlet')
    filter_content_types=1

    def canSetDefaultPage(self):
        return False    
    
    def getInheritedCategories(self):
        """ Traverse upwards in the tree to collect all the available categories."""
        cats=[]
        parent=self.aq_parent
        portal=self.portal_url.getPortalObject()
        categories='<ul>'
        while parent!=portal:
            if parent.portal_type=='Blog' or parent.portal_type=='BlogFolder':
                # add cats
                pcats=parent.getCategories()
                for c in pcats:
                    if c not in cats:
                        categories=categories + '<li>' + c + '</li>'
                        cats.append(c)
                if parent.portal_type=='Blog':
                    break
            parent=parent.aq_parent
        categories = categories + '</li>'
        if len(cats)==0:
            return '-'
        else:
            return categories

    def getEntries(self, maxResults=None, **kwargs):
        """ Return all the contained published entries, real objects, not the brains """
        blog = self.simpleblog_tool.getFrontPage(self)
        kwargs.update({'path':{'query':'/'+'/'.join(self.getPhysicalPath()),'level':0}})
        return blog.getEntries(maxResults=maxResults, **kwargs)


    def synContentValues(self):
        entries = self.simpleblog_tool.searchForEntries(self, fromHere=1, maxResults=0)
        objs = [e.getObject() for e in entries]
        return objs

registerType(BlogFolder)
