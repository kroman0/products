from Products.Archetypes.public import BaseSchema, BaseFolderSchema, Schema
from Products.Archetypes.public import StringField, TextField, LinesField, BooleanField, ReferenceField
from Products.Archetypes.public import TextAreaWidget, VisualWidget,  MultiSelectionWidget, StringWidget, IdWidget, LinesWidget, KeywordWidget, SelectionWidget
from Products.Archetypes.public import RichWidget, BooleanWidget
from Products.Archetypes.public import BaseContent, registerType, BaseFolder
from Products.CMFCore import CMFCorePermissions

from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import ManageProperties

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *
from DateTime import DateTime
from Products.SimpleBlog.Permissions import CROSS_POST_PERMISSION
from Products.SimpleBlog.config import ENTRY_IS_FOLDERISH
from Products.SimpleBlog.util import post_trackback
from Products.ATContentTypes.content.document import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent, ATCTFolder

from Products.CMFCore.utils import getToolByName
import string,os,urllib,httplib,urlparse,re
import sys
from Products.SimpleBlog.util import *
from Products.SimpleBlog.config import DIGG_TOPICS

if ENTRY_IS_FOLDERISH:
    schema = ATCTFolder.schema.copy()
    parentClass = ATCTFolder
else:
    schema = ATCTContent.schema.copy()
    parentClass = ATCTContent

schema = schema +  Schema((
    StringField('description',
                searchable=1,
                isMetadata=1,
                accessor='Description',
                widget=TextAreaWidget(label='Description', 
                                    label_msgid="label_entry_description",
                                    description_msgid="help_entry_description",
                                    i18n_domain="SimpleBlog",
                                    description='Give a description for this entry.')),
    TextField('body',
              searchable=1,
              required=0,
              primary=1,
              default_content_type='text/html',
              default_output_type='text/html',
              allowable_content_types=('text/plain','text/structured', 'text/html', 'text/restructured'),
              widget=RichWidget(label='Body',
                                label_msgid="label_entry_body",
                                description_msgid="help_entry_body",
                                i18n_domain="SimpleBlog",
                                description="")),
    
    ReferenceField('crossPosts',
                   multiValued=1,
                   required=0,
                   relationship='AppearsIn',
                   write_permission=CROSS_POST_PERMISSION,
                   allowed_types=('Blog',),
                   widget=ReferenceBrowserWidget(condition="python:0", # this line have to be removed in order to be visible/editable
                            force_close_on_insert=1, 
                            i18n_domain="SimpleBlog",
                            label_msgid="label_crosspost",
                            description_msgid="help_crosspost",
                            label='Cross posts', 
                            description='Select one or more other blogs where this entry will appear in when published additionally to this blog.')),
    BooleanField('alwaysOnTop', 
             default=0,
             index='FieldIndex:schema',
             widget=BooleanWidget(label='Entry is always listed on top', 
                           label_msgid="label_always_top",
                           description_msgid="help_always_top",
                           i18n_domain="SimpleBlog",
                           description='Controls if the Entry (when published) shown as the first Entry. If not checked, the effective date is used.')),
    LinesField('categories',
                    accessor='EntryCategory', 
                    edit_accessor='EntryCategory', 
                    index='KeywordIndex', 
                    vocabulary='listCategories',
                    widget=MultiSelectionWidget(format='select', 
                           label_msgid="label_entry_categories",
                           description_msgid="help_entry_categories",
                           i18n_domain="SimpleBlog",
                           label='Categories', 
                           description='Select to which categories this Entry belongs to')),
    LinesField('tags',
                    accessor = 'EntryTag', 
                    mutator = 'setEntryTag',    
                    index = 'KeywordIndex', 
                    enforseVocabulary = 1,      
                    vocabulary = 'listTags',    
                    widget = KeywordWidget(label_msgid = "label_entry_tags",
                           description_msgid = "help_entry_tags",
                           i18n_domain = "SimpleBlog",
                           label = 'Tags', 
                           description = 'Select tags for technorati.com')),

    BooleanField('alwaysOnTop', 
             default = 0,
             index = 'FieldIndex:schema',
             widget = BooleanWidget(label = 'Entry is always listed on top.', 
                           label_msgid = "label_always_top",
                           description_msgid = "help_always_top",
                           i18n_domain = "SimpleBlog",
                           description = 'Controls if the Entry (when published) shown as the first Entry. If not checked, the effective date is used.')),
    LinesField('sendTrackBackURLs',
               languageIndependent = True,
               searchable = True,
               widget = LinesWidget(label = "sendTrackBackURLs",
                                  label_msgid = "label_sendTrackBackURLs",
                                  description = ("URL for sending trackbacks"),
                                  description_msgid = "help_event_attendees",                 
                                  i18n_domain = "plone")),
    StringField('diggTopic',
                default='offbeat_news',
                vocabulary=DIGG_TOPICS,
                widget=SelectionWidget(label='Digg topic',
                        label_msgid="label_digg_topic",
                        description_msgid="help_digg_topic",
                        i18n_domain="SimpleBlog",
                        description='Choose the digg topic.')),
     ))

# Finalise the schema according to ATContentTypes standards. This basically
# moves the Related items and Allow discussion fields to the bottom of the
# form. See ATContentTypes.content.schemata for details.
finalizeATCTSchema(schema)


class BlogEntry(parentClass):
    """
    A BlogEntry can exist inside a SimpleBlog Folder or an EntryFolder
    """
    # Standard content type setup
    portal_type = meta_type = 'BlogEntry'
    archetype_name = 'Blog Entry'
    content_icon='entry_icon.gif'
    schema = schema
    global_allow=0
    allow_discussion = 1

    default_view = 'blogentry_view'
    immediate_view = 'blogentry_view'

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    if ENTRY_IS_FOLDERISH:
        filter_content_types=1
        allowed_content_types=('TrackBack') #('Link', 'Image', 'File', 'TrackBack')


    def canSetDefaultPage(self):
        return False


    def getAlwaysOnTop(self):
        if hasattr(self, 'alwaysOnTop'):
            if self.alwaysOnTop==None or self.alwaysOnTop==0:
                return 0
            else:
                return 1
        else:
            return 0
            
    def getIcon(self, relative_to_portal=0):
        try:
            if self.getAlwaysOnTop()==0:
                return 'entry_icon.gif'
            else:
                return 'entry_pin.gif'
        except:
            return 'entry_icon.gif'
        
    def listCategories(self):
        # traverse upwards in the tree to collect all the available categories
        # stop collecting when a SimpleBlog object is reached
        
        cats=[]
        parent=self.aq_parent
        portal=self.portal_url.getPortalObject()
        
        while parent!=portal:
           if parent.portal_type=='Blog' or parent.portal_type=='BlogFolder':
               # add cats
               pcats=parent.getCategories()
               for c in pcats:
                   if c not in cats:
                       cats.append(c)
               if parent.portal_type=='Blog':
                   break
           parent=parent.aq_parent
           
        # add the global categories
        for c in self.simpleblog_tool.getGlobalCategories():
            if not c in cats:
                cats.append(c)           
        cats.sort()
        return tuple(cats)

    def start(self):
        return self.getEffectiveDate()
        
    def end(self):
        """ 
        return the same data as start() since an entry is not an event but an item that is published on a specific
        date. We want the entries in the calendar to appear on only one day.
        """
        return self.getEffectiveDate()




# =============================

    #function for sending ping
    def sendTrackBack(self):
        message = "TrackBack sent"
        title = self.title
        src_url = self.absolute_url()
        blog = self.simpleblog_tool.getFrontPage(self)
        blog_name = blog.Title()
        excerpt=self.description
        agent = "SimpleBlog"
        result=[]
        for i in self.getSendTrackBackURLs():
            ping_url=i
            err,mes = post_trackback(self,
                                     ping_url=ping_url, 
                                     title = title,
                                     src_url = src_url,
                                     blog_name = blog_name,
                                     excerpt=self.description,
                                     agent = "SimpleBlog",
                                     charset = "utf-8")
            result.append((err,mes))
        result.append(("excerpt",self.description))
        return result

    def getTrackbacks(self):
        """ """
        return self.listFolderContents(spec="TrackBack")

    def setEntryTag(self, value, **kwargs):
        """ Update tags in the Entry in parent Blog """
        value = list(value)
        value.sort()
        self.getField('tags').set(self, value, **kwargs)

        tags = self.listTags()
        newEntries = [v for v in value if not v in tags]
        if not newEntries:
            return
        newTagsList = list(tags)+ list(newEntries)
        parent = self.aq_parent
        portal = self.portal_url.getPortalObject()
        while parent != portal:
           if parent.portal_type == 'Blog':
               break
           parent = parent.aq_parent
        parent.setTags(newTagsList, **kwargs)

    def listTags(self):
        """ Get the list of Tags from parent Blog """
        tags = []
        parent = self.aq_parent
        portal = self.portal_url.getPortalObject()
        while parent != portal:
           if parent.portal_type == 'Blog':
               tags = parent.getTags()
               break
           parent = parent.aq_parent
        return tuple(tags)


registerType(BlogEntry)
