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

from Products.ATContentTypes.content.base import  ATCTBTreeFolder, ATCTFolder
from Products.ATContentTypes.lib.constraintypes import  ConstrainTypesMixinSchema

schema = ConstrainTypesMixinSchema.copy() + ATCTFolder.schema.copy() +  Schema((
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
schema['relatedItems'].widget.visible={'view' : 'invisible', 'edit':'invisible'}

class Blog(ATCTBTreeFolder,ATCTFolder):
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

        self.metaWeblog = MetaWeblogAPI.MetaWeblogAPI().__of__(self)
        self.metaWeblog.setupRPCAuth(RPCAuth)
        self.blogger = BloggerAPI.BloggerAPI().__of__(self)
        self.blogger.setupRPCAuth(RPCAuth)
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
        syn_tool = getToolByName(self, 'portal_syndication')
        limit = int(syn_tool.getMaxItems(self))
        entries = self.getEntries(maxResults=limit)[1]
        objs = [e.getObject() for e in entries]
        return objs

    def listCategories(self):
        cats=self.getCategories()

        for c in self.simpleblog_tool.getGlobalCategories():
            if not c in cats:
                cats.append(c)
        cats = list(cats)
        cats.sort()
        return tuple(cats)

    def getForeignEntries(self):
        """ Returns all entries from other blogs that are published into this blog using the remoteBlogs value """
        return [f for f in self.getBRefs('AppearsIn') if self.portal_membership.checkPermission('View', f)]

    def buildBatch(self, b_start, query, notlimited_len):
        """Return batch for navigation"""
        #if 'getAlwaysOnTop' in query.keys():
            #query['getAlwaysOnTop']=1
            #len1 = len(self.portal_catalog(**query))
            #query['getAlwaysOnTop']=0
        if 'sort_limit' in query.keys():
            del query['sort_limit']
            total_len = len(self.portal_catalog(**query))
        else:
            total_len = notlimited_len
        ditems = self.getDisplayItems()
        
        batch = []
        if total_len > ditems:
            max_pages = total_len/ditems + (total_len%ditems and 1 or 0)
            vis_middle = 3  # max number of pages in one of the side around current
            curr_num = b_start/ditems >= max_pages and max_pages or b_start/ditems+1
            # first page (when current page far from 1st page)
            first = []
            if curr_num-vis_middle > 2:
                first = [1,"b_start=0"]
            batch.append(first)
            # last page (when current page far from terminal page)
            last = []
            if max_pages-curr_num > vis_middle+1:
                last = [max_pages,"b_start=%d" % ((max_pages-1)*ditems)]
            batch.append(last)
            # form batch around current page
            lft_bound =  curr_num-vis_middle > 2 and curr_num-vis_middle or 1
            rght_bound = max_pages-curr_num > vis_middle+1 and curr_num+vis_middle or max_pages
            lst = []
            for p in range(lft_bound, rght_bound+1):
                q = p!=curr_num and "b_start=%d" % ((p-1)*ditems) or ""
                lst.append([p,q])
            batch.append(lst)
        return batch

    def getStart(self):
        """ Validate b_start from request and return right value."""
        request = self.REQUEST
        try:
            b_start = int(request.get('b_start', 0)) or 0
        except:
            b_start = 0
        if b_start < 0:
            b_start = 0
        return b_start

    def getEntries(self, category=None, maxResults=None, b_start=0, filterState=1, join=0, skipOnTop=0, mode="", **kwargs):
        """ Return all the contained published entries, real objects, not the brains """
        query=kwargs
        publishedState = self.simpleblog_tool.getPublishedState()
        if category!=None:
            query['EntryCategory']=category
        if filterState:
            query['review_state']=publishedState
        if maxResults:
            query['sort_limit'] = maxResults + 1 # need to if the last page riched
        if not query.has_key('path'):
            query['path'] = {'query':self.simpleblog_tool.getObjectPath(self),'level':0}
        query['sort_order'] = 'reverse'
        query['sort_on'] = 'effective'
        query['meta_type'] = 'BlogEntry'
        onTop = []
        if not skipOnTop and b_start==0:
            query['getAlwaysOnTop']=1
            onTop = list(self.portal_catalog.searchResults(query))
            query['getAlwaysOnTop']=0

        onBottom = list(self.portal_catalog.searchResults(query))
        ####  cut the b_start when it is tooo large
        itemsPerPage = self.getDisplayItems()
        last = 0
        if len(onBottom) < maxResults + 1: #last page
            last = 1
        elif len(onBottom) == maxResults + 1: #not last page yet
            onBottom = onBottom[:-1]
        if len(onBottom) < b_start:  # too large b_start given
            b_start = (len(onBottom)/itemsPerPage)*itemsPerPage
        if join:
            results = onTop+onBottom
            batch = 'navigation' in query.keys() and self.buildBatch(b_start, query, len(results)) or []
            if b_start > 0:
                if len(onBottom) == b_start:
                    b_start = b_start-(maxResults-b_start)
                    last = 1
                results = results[b_start:]
            return (results,last,batch)
        else:
            batch = 'navigation' in query.keys() and self.buildBatch(b_start, query, len(onBottom)) or []
            return (onTop, onBottom, batch)

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

