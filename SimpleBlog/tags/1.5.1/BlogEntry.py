from Products.Archetypes.public import *

#from Products.Archetypes.public import BaseSchema, BaseFolderSchema, Schema
#from Products.Archetypes.public import StringField, TextField, LinesField, BooleanField
#from Products.Archetypes.public import TextAreaWidget, VisualWidget,  MultiSelectionWidget, StringWidget, IdWidget
#from Products.Archetypes.public import RichWidget, BooleanWidget
#from Products.Archetypes.public import BaseContent, registerType, BaseFolder
from Products.CMFCore import CMFCorePermissions

from Products.CMFCore.utils import getToolByName

from DateTime import DateTime

import Permissions
import string,os,urllib,httplib,urlparse,re
import sys
from util import *
from config import DIGG_TOPICS

schema  =  BaseFolderSchema +  Schema((
     StringField('id',
                 required = 0, ## Still actually required, but
                             ## the widget will supply the missing value
                             ## on non-submits
                 mode = "rw",
                 accessor = "getId",
                 mutator = "setId",
                 default = None,
                 widget = IdWidget(label = "Short Name",
                                   label_msgid = "label_short_name",
                                   description = "Should not contain spaces, underscores or mixed case. "\
                                                 "Short Name is part of the item's web address.",
                                   description_msgid = "help_shortname",
                                   visible = {'view' : 'visible', 'edit':'visible'},
                                   i18n_domain = "plone"),
                 ),
    StringField('title',
                required = 1,
                searchable = 1,
                default = '',
                accessor = 'Title',
                widget = StringWidget(label_msgid = "label_title",
                                    description_msgid = "help_title",
                                    i18n_domain = "plone"),
                ),    
    StringField('description',
                searchable = 1,
                isMetadata = 1,
                accessor = 'Description',
                widget = TextAreaWidget(label = 'Description', 
                                    label_msgid = "label_entry_description",
                                    description_msgid = "help_entry_description",
                                    i18n_domain = "SimpleBlog",
                                    raws = 3, 
                                      description = 'Give a description for this entry.'),),
    TextField('body',
              searchable = 1,
              required = 0,
              primary = 1,
              default_content_type = 'text/html',
              default_output_type = 'text/html',
              allowable_content_types = ('text/plain','text/structured', 'text/html', 'text/restructured'),
              widget = RichWidget(label = 'Body',
                                label_msgid = "label_entry_body",
                                description_msgid = "help_entry_body",
                                i18n_domain = "SimpleBlog",
                                description = "Body of the blog")),

    LinesField('categories',
                    accessor = 'EntryCategory', 
                    edit_accessor = 'EntryCategory', 
                    index = 'KeywordIndex', 
                    vocabulary = 'listCategories',
                    widget = MultiSelectionWidget(format = 'select', 
                           label_msgid = "label_entry_categories",
                           description_msgid = "help_entry_categories",
                           i18n_domain = "SimpleBlog",
                           label = 'Categories', 
                           description = 'Select to which categories this Entry belongs to')),
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

    BooleanField('enableTopAdsence',
                 widget = BooleanWidget(format = 'select', 
                           label_msgid = "label_enable_top_adsence",
                           description_msgid = "help_enable_top_adsence",
                           i18n_domain = "SimpleBlog",
                           label = 'Enable top Adsence block',
                           description = None)),
    StringField('topAdsence',
                vocabulary = 'listAdesnceTemplates',
                widget = SelectionWidget(format = 'select', 
                        label_msgid = "label_top_adsence",
                        description_msgid = "help_top_adsence",
                        i18n_domain = "SimpleBlog",
                        label = 'Top Adsence',
                        description = None)),
    BooleanField('enableBottomAdsence',
                 widget = BooleanWidget(format = 'select', 
                           label_msgid = "label_enable_bottom_adsence",
                           description_msgid = "help_enable_bottom_adsence",
                           i18n_domain = "SimpleBlog",
                           label = 'Enable bottom Adsence block',
                           description = None)),
    StringField('bottomAdsence',
                vocabulary = 'listAdesnceTemplates',
                widget = SelectionWidget(format = 'select', 
                        label_msgid = "label_bottom_adsence",
                        description_msgid = "help_bottom_adsence",
                        i18n_domain = "SimpleBlog",
                        label = 'Bottom Adsence',
                        description = None)),
    StringField('diggTopic',
                default='offbeat_news',
                vocabulary=DIGG_TOPICS,
                widget=SelectionWidget(label='Digg topic',
                        label_msgid="label_digg_topic",
                        description_msgid="help_digg_topic",
                        i18n_domain="SimpleBlog",
                        description='Choose the digg topic.')),
    ))


class BlogEntry(BaseFolder):
    """
    A BlogEntry can exist inside a SimpleBlog Folder or an EntryFolder
    """

    schema  =  schema

    global_allow = 0
    
    content_icon = 'entry_icon.gif'
    
    filter_content_types = 1
    allowed_content_types = ('TrackBack','Link', 'Image', 'File')
    
    actions  =  ({
       'id': 'view',
        'name': 'View',
        'action': 'string:${object_url}/blogentry_view',
        'permissions': (CMFCorePermissions.View,)
        },
        {'id': 'references',
          'name': 'References',
          'action': 'string:${object_url}/reference_edit',
          'permissions': (CMFCorePermissions.ModifyPortalContent,),
          'visible':0},
        {'id': 'metadata',
          'name': 'Properties',
          'action': 'string:${object_url}/base_metadata',
          'permissions': (CMFCorePermissions.ModifyPortalContent,),
          'visible':0})


    

    def getAlwaysOnTop(self):
        if hasattr(self, 'alwaysOnTop'):
            if self.alwaysOnTop == None or self.alwaysOnTop == 0:
                return 0
            else:
                return 1
        else:
            return 0
            
    def getIcon(self, relative_to_portal = 0):
        try:
            if self.getAlwaysOnTop() == 0:
                return 'entry_icon.gif'
            else:
                return 'entry_pin.gif'
        except:
            return 'entry_icon.gif'
        
    def listCategories(self):
        # traverse upwards in the tree to collect all the available categories
        # stop collecting when a SimpleBlog object is reached
        
        cats = []
        parent = self.aq_parent
        portal = self.portal_url.getPortalObject()
        
        while parent != portal:
           if parent.portal_type == 'Blog' or parent.portal_type == 'BlogFolder':
               # add cats
               pcats = parent.getCategories()
               for c in pcats:
                   if c not in cats:
                       cats.append(c)
               if parent.portal_type == 'Blog':
                   break
           parent = parent.aq_parent
           
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

    def listAdesnceTemplates(self):
        """ return list of available adsence blocks """
        pp = getToolByName(self, 'portal_properties')
        templates = ()
        try:
            templates = pp.simpleblog_properties.getProperty('adsence_templates',())
        except:
            pass
        return templates

registerType(BlogEntry)
