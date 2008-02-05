from Products.Archetypes.public import BaseFolderSchema, Schema
from Products.Archetypes.public import StringField, LinesField, IntegerField, BooleanField
from Products.Archetypes.public import SelectionWidget, LinesWidget, TextAreaWidget, MultiSelectionWidget, IntegerWidget, RichWidget, IdWidget, StringWidget, BooleanWidget
from Products.Archetypes.public import BaseFolder, registerType
from Products.Archetypes.public import DisplayList

from Products.CMFCore import CMFCorePermissions
from DateTime import DateTime
from Products.SimpleBlog.config import DISPLAY_MODE, ENABLE_ADSENSE
import Products.SimpleBlog.Permissions
from Products.CMFCore.utils import getToolByName

from Products.SimpleBlog import MetaWeblogAPI
from Products.SimpleBlog import BloggerAPI
from Products.SimpleBlog import MovableTypeAPI
from Products.Archetypes.utils import  unique

from Products.ATContentTypes.content.base import ATCTFolder

schema = ATCTFolder.schema.copy() +  Schema((
    StringField('description',
                isMetadata=1,
                accessor='Description',
                searchable=1,
                widget=TextAreaWidget(label='Description',
                                      label_msgid="label_blog_description",
                                      description_msgid="help_blog_description",
                                      i18n_domain="SimpleBlog",
                                      description='Give a description for this SimpleBlog.')),
    # this field is deprecated, here for compatibility
    StringField('displayMode',
                vocabulary=DISPLAY_MODE,
                widget=SelectionWidget(label='Display Mode', 
                                       label_msgid="label_display_mode",
                                       description_msgid="help_display_mode",
                                       i18n_domain="SimpleBlog",
                                       description='Choose the display mode.',
                                       visible={'view' : 'invisible', 'edit':'invisible'}),
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
                                  description='Supply the list of possible categories that can be used in SimpleBlog Entries.')),
    BooleanField('allowCrossPosting',
             default=0, 
             widget=BooleanWidget(condition="python:0", # hide the field
                        label='Allow cross-posting',
                        i18n_domain="SimpleBlog",
                        label_msgid="label_allowCrossPosting",
                        description_msgid="help_allowCrossPosting",
                        description='When checked, this blog will include cross-post entries from other blogs.')),
    LinesField('tags',
               mutator = 'setTags',
               widget=LinesWidget(label="Tags",
                                  description='List of tags.'),
               ),
    BooleanField('warnForUnpublishedEntries', 
               default=1,
               schemata = 'interface',
               widget=BooleanWidget(label='Show unpublished entries warning', 
                      i18n_domain="SimpleBlog",
                      label_msgid="label_warnForUnpublishedEntries",
                      description_msgid="help_warnForUnpublishedEntries",
                      description='When checked, a warning will be displayed on the blog\'s frontpage if there are entries that are not yet published.')),
    BooleanField('showByline',
                  default = 1,
                  schemata = 'interface',
                  widget=BooleanWidget(label="Show Byline footer",
                                       label_msgid="label_show_buttons",
                                       description_msgid="help_show_buttons",),
               ),
    BooleanField('showIcons',
                  default = 1,
                  schemata = 'interface',
                  widget=BooleanWidget(label="Show Icons",
                                       label_msgid="label_show_icons",
                                       description_msgid="help_show_icons",),
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
    # used to be new trackbaks notification email address
    StringField('adminEmail',
                accessor = 'getAdminEmail',
                mutator = 'setAdminEmail',
                schemata = 'interface',
                default = '',
                widget=StringWidget(label="Administrator's email", 
                                    label_msgid="label_adminEmail",
                                    description_msgid="help_adminEmail",
                                    i18n_domain="SimpleBlog",
                                    condition="python:0", # this line have to be removed in order to be visible/editable
                                    description="Enter administrator's email for receiving notification about blog's activity"),
               ),
    BooleanField('allowDelicious',
                default = 1,
                accessor = 'isDeliciousEnabled',
                schemata = 'interface', 
                widget=BooleanWidget(label="Turn Delicious bookmarklet",
                                    label_msgid="label_allow_delicious",
                                    description_msgid="help_allow_delicious"),
                ),
    BooleanField('allowDigg',
                default = 1,
                accessor = 'isDiggEnabled',
                schemata = 'interface',
                widget=BooleanWidget(label="Turn Digg bookmarklet",
                                    label_msgid="label_allow_digg",
                                    description_msgid="help_allow_digg"),
                ),
    BooleanField('allowYahoo',
                default = 1,
                accessor = 'isYahooEnabled',
                schemata = 'interface', 
                widget=BooleanWidget(label="Turn Yahoo bookmarklet",
                                    label_msgid="label_allow_yahoo",
                                    description_msgid="help_allow_yahoo"),
                ),
    BooleanField('allowGoogle',
                default = 1,
                accessor = 'isGoogleEnabled',
                schemata = 'interface',
                widget=BooleanWidget(label="Turn Google bookmarklet",
                                    label_msgid="label_allow_google",
                                    description_msgid="help_allow_google"),
                ),
    BooleanField('allowSpurl',
                default = 1,
                accessor = 'isSpurlEnabled',
                schemata = 'interface', 
                widget=BooleanWidget(label="Turn Spurl bookmarklet",
                                    label_msgid="label_allow_spurl",
                                    description_msgid="help_allow_spurl"),
                ),
    BooleanField('enableTopAdsence',
                 schemata = 'interface',
                 default=0,
                 accessor = 'isTopAdsenceEnabled',
                 widget = BooleanWidget(format = 'select',
                           label = 'Turn top Adsence block',
                           label_msgid = "label_enable_top_adsence",
                           description_msgid = "help_enable_top_adsence",
                           i18n_domain = "SimpleBlog",
                           description = None,
                           condition="python:%s" % ENABLE_ADSENSE)),
    StringField('topAdsence',
                schemata = 'interface',
                vocabulary = 'listAdsenseTemplates',
                widget = SelectionWidget(format = 'select',
                        label = 'Select top adsence template',
                        label_msgid = "label_top_adsence",
                        description_msgid = "help_top_adsence",
                        i18n_domain = "SimpleBlog",
                        description = None,
                        condition="python:%s" % ENABLE_ADSENSE)),
    BooleanField('enableBottomAdsence',
                 schemata = 'interface',
                 default=0,
                 accessor = 'isBottomAdsenceEnabled',
                 widget = BooleanWidget(format = 'select',
                           label = 'Turn bottom adsence block',
                           label_msgid = "label_enable_bottom_adsence",
                           description_msgid = "help_enable_bottom_adsence",
                           i18n_domain = "SimpleBlog",
                           description = None,
                           condition="python:%s" % ENABLE_ADSENSE)),
    StringField('bottomAdsence',
                schemata = 'interface', 
                vocabulary = 'listAdsenseTemplates',
                widget = SelectionWidget(format = 'select',
                        label = 'Select bottom adsence',
                        label_msgid = "label_bottom_adsence",
                        description_msgid = "help_bottom_adsence",
                        i18n_domain = "SimpleBlog",
                        description = None,
                           condition="python:%s" % ENABLE_ADSENSE)),
        ))

# hide relatedItems
schema['relatedItems'].widget.visible={'view' : 'invisible', 'edit':'invisible'}

class Blog(ATCTFolder):
    """Blog"""

    portal_type = meta_type = 'Blog'
    archetype_name = 'Blog'
    content_icon='simpleblog_icon.gif'
    schema = schema
    global_allow=1

    default_view = 'simpleblog_view_title_description'
    immediate_view = 'simpleblog_view_title_description'
    suppl_views = ('simpleblog_view_title_description', 'simpleblog_view_title', 'simpleblog_view_title_description_body')

    filter_content_types=1    
    allowed_content_types=('BlogEntry', 'BlogFolder', 'Link', 'Image', 'File', 'Portlet')

    blogger = None
    metaWeblog = None

    def initializeArchetype(self, **kwargs):
        BaseFolder.initializeArchetype(self, **kwargs)
        RPCAuth = self.simpleblog_tool.findRPCAuth(self)

        # Setup the MetaWeblog API
        self.metaWeblog = MetaWeblogAPI.MetaWeblogAPI().__of__(self)
        self.metaWeblog.setupRPCAuth(RPCAuth)

        # Setup the Blogger API
        self.blogger = BloggerAPI.BloggerAPI().__of__(self)
        self.blogger.setupRPCAuth(RPCAuth)

        # Setup the MovableTypeAPI API
        self.mt = MovableTypeAPI.MovableTypeAPI().__of__(self)
        self.mt.setupRPCAuth(RPCAuth)    

    def canSetDefaultPage(self):
        return False

    def manage_afterAdd(self, item, container):
        BaseFolder.manage_afterAdd(self, item, container)
        if self.simpleblog_tool.getCreatePortletOnBlogCreation():
            if not hasattr(item.aq_base, 'right_slots'):
                item._setProperty('right_slots', ['here/portlet_simpleblog/macros/portlet'], 'lines')

    def synContentValues(self):
        # get brains for items that are published within the context of this blog.
        entries = self.simpleblog_tool.searchForEntries(self, maxResults=0)

        # convert to objects
        objs = [e.getObject() for e in entries]
        return objs

    def listCategories(self):
        cats=self.getCategories()

        # add the global categories
        for c in self.simpleblog_tool.getGlobalCategories():
            if not c in cats:
                cats.append(c)
        cats = list(cats)
        cats.sort()
        return tuple(cats)

    def getForeignEntries(self):
        """ Returns all entries from other blogs that are published into this blog using the remoteBlogs value """
        return [f for f in self.getBRefs('AppearsIn') if self.portal_membership.checkPermission('View', f)]

    def getEntries(self, category=None, maxResults=None, fromHere=0, filterState=1, sort=1, join=0, addCrossPostInfo=0, skipOnTop=0, **kwargs):
        """ Return all the contained published entries, real objects, not the brains """
        # see simpleblog_tool.searchForEntries for API description
        query=kwargs
        publishedState = self.simpleblog_tool.getPublishedState()
        if category!=None:
            query['EntryCategory']=category
        if filterState:
            query['review_state']=publishedState
        if maxResults:
            query['sort_limit'] = maxResults
        query['path'] = {'query':self.simpleblog_tool.getObjectPath(self),'level':0}
        query['sort_order'] = 'reverse'
        query['sort_on'] = 'effective'
        query['meta_type'] = 'BlogEntry'
        if not skipOnTop:
            query['getAlwaysOnTop']=1
            # first the items that need to be listed on top
            localOnTop = self.portal_catalog.searchResults(query)
            localOnTop = [r.getObject() for r in localOnTop ]
            # then the other items
            query['getAlwaysOnTop']=0
        else:
            localOnTop = []
        localNoTop = self.portal_catalog.searchResults(query)
        localNoTop= [r.getObject() for r in localNoTop]

        onTop = localOnTop
        onBottom = localNoTop
        if join:
            results = onTop+onBottom
            if maxResults==0:
                return results
            elif maxResults==None:
                return results[:self.simpleblog_tool.getMaxItemsInPortlet()]
            else:
                return results[:maxResults]
        else:
            return (onTop, onBottom)

    def getAdminEmail(self):
        """ return blog admin email or root email """
        val = self.getField('adminEmail').get(self)
        if not val:
            purl = getToolByName(self, 'portal_url')
            val = purl.getPortalObject().getProperty("trackback_notification_email", "")
        return val

    def setTags(self, value, **kwargs):
        """ Save tags in lower case """
        value = unique(value)
        value.sort(lambda x, y: cmp(x,y))
        self.getField('tags').set(self, value, **kwargs)

    def listAdsenseTemplates(self):
        """ Return DisplayList of available adsence blocks """
        try:
            from Products.adsenseproduct.util import getAdsenseMap
        except:
            return ()
        templates = [(key, value['title']) for key, value in getAdsenseMap().items()]
        return DisplayList(templates)

registerType(Blog)

