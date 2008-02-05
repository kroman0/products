from Products.Archetypes.public import *
from Products.Archetypes.utils import  unique
from Products.CMFCore import CMFCorePermissions
from DateTime import DateTime
from config import DISPLAY_MODE
import Permissions
from Products.CMFCore.utils import getToolByName

schema = BaseFolderSchema +  Schema((
    StringField('id',
                required=0, ## Still actually required, but
                            ## the widget will supply the missing value
                            ## on non-submits
                mode="rw",
                accessor="getId",
                mutator="setId",
                default=None,
                widget=IdWidget(label="Short Name",
                                label_msgid="label_short_name",
                                description="Should not contain spaces, underscores or mixed case. "\
                                            "Short Name is part of the item's web address.",
                                description_msgid="help_shortname",
                                visible={'view' : 'visible'},
                                i18n_domain="plone"),
                ),
    StringField('title',
                required=1,
                searchable=1,
                default='',
                accessor='Title',
                widget=StringWidget(label_msgid="label_title",
                                    description_msgid="help_title",
                                    i18n_domain="plone"),
                ),
    StringField('description',
                isMetadata=1,
                accessor='Description',
                searchable=1,                
                widget=TextAreaWidget(label='Description', 
                                      label_msgid="label_blog_description",
                                      description_msgid="help_blog_description",
                                      i18n_domain="SimpleBlog",
                                      description='Give a description for this SimpleBlog.'),),
    StringField('displayMode',
                vocabulary=DISPLAY_MODE,
                widget=SelectionWidget(label='Display Mode', 
                                       label_msgid="label_display_mode",
                                       description_msgid="help_display_mode",
                                       i18n_domain="SimpleBlog",
                                       description='Choose the display mode.'),
                default='descriptionOnly'),
    IntegerField('displayItems', 
                widget=IntegerWidget(label='BlogEntries to display', 
                                      label_msgid="label_display_items",
                                      description_msgid="help_display_items",
                                      i18n_domain="SimpleBlog",
                                      description='Set the maximum number of BlogEntries to display.'), 
                 default=20),
    LinesField('categories',
               widget=LinesWidget(label='Possible Categories', 
                                  label_msgid="label_categories",
                                  description_msgid="help_categories",
                                  i18n_domain="SimpleBlog",
                                  description='Supply the list of possible categories that can be used in SimpleBlog Entries.'),
               ),
    LinesField('tags',
               mutator = 'setTags',
               widget=LinesWidget(label="Tags",
                                  description='List of tags.'),
               ),
    BooleanField('tagsEnabled',
                  accessor = 'isTagsEnabled',
                  default = 1,
                  schemata = 'interface',
                  widget = BooleanWidget(label='Enable technorati tags',
                                     label_msgid="label_enable_tags",
                                     description_msgid="help_enable_tags",),
              ),
    BooleanField('allowTrackback',
                  default = 1,
                  schemata = 'interface', 
                  widget=BooleanWidget(label="Allow Trackback", 
                                       label_msgid="label_allow_trackback",
                                       description_msgid="help_allow_trackback",),
               ),
    StringField('adminEmail',
                accessor = 'getAdminEmail',
                mutator = 'setAdminEmail',
                schemata = 'interface',
                default = '',
                widget=StringWidget(label="Administrator's email", 
                                    label_msgid="label_adminEmail",
                                    description_msgid="help_adminEmail",
                                    i18n_domain="SimpleBlog",
				                    condition="python:0",
                                    description="Enter administrator's email for receaving notification about blog's activity"),
               )
    #BooleanField('allowComments',
    #              default = 1,
    #              schemata = 'interface', 
    #              widget=BooleanWidget(label="Allow Comments", 
    #                                   label_msgid="label_allow_comments",
    #                                   description_msgid="help_allow_comments",),
    #           ),
    #BooleanField('expandMainPageComments',
    #              default = 0,
    #              schemata = 'interface',
    #              widget = BooleanWidget(label='Expand comments on main page', 
    #                                 label_msgid="label_expand_mainpage_comments",
    #                                 description_msgid="help_expand_mainpage_comments",),
    #          ),

        ))


class Blog(BaseFolder):
    """
Blog
    """
    allowed_content_types=('BlogEntry', 'BlogFolder', 'Link', 'Image', 'File', 'Portlet')
    filter_content_types=1    
    global_allow=1
    schema=schema
    
    content_icon='simpleblog_icon.gif'

    actions = ({'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/simpleblog_view',
                'permissions': (CMFCorePermissions.View,) },
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

    def manage_afterAdd(self, item, container):
        BaseFolder.manage_afterAdd(self, item, container)
        if self.simpleblog_tool.getCreatePortletOnBlogCreation():
            if not hasattr(item.aq_base, 'right_slots'):
                item._setProperty('right_slots', ['here/portlet_simpleblog/macros/portletBlogFull_local'], 'lines')
            if not hasattr(item.aq_base, 'column_two_portlets'):
                item._setProperty('column_two_portlets', ['here/portlet_simpleblog/macros/portletBlogFull_local'], 'lines')

    def synContentValues(self):
        # get brains for items that are published within the context of this blog.
        entries = self.simpleblog_tool.searchForEntries(self, maxResults=0)

        # convert to objects
        objs = [e.getObject() for e in entries]
        return objs

    def setTags(self, value, **kwargs):
        """ Save tags in lower case """
        value = unique(value)
        value.sort(lambda x, y: cmp(x,y))
        self.getField('tags').set(self, value, **kwargs)

    def getAdminEmail(self):
        """ return blog admin email or root email """
        val = self.getField('adminEmail').get(self)
        if not val:
            purl = getToolByName(self, 'portal_url')
            val = purl.getPortalObject().getProperty("trackback_notification_email", "")
        return val

registerType(Blog)

