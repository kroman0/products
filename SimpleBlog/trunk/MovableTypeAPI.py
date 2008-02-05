
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
import xmlrpclib
from OFS.SimpleItem import SimpleItem

XMLRPCTRUE = xmlrpclib.Boolean(1)
XMLRPCFALSE = xmlrpclib.Boolean(0)

authTwoMethods = ['mt/getRecentPostTitles', 'mt/getPostCategories',
                  'mt/setPostCategories', 'mt/publishPost',
                  'mt/supportedMethods', 'mt/supportedTextFilters']


def genericBloggerAuthTwo(arg_tuple):
     return arg_tuple[1],arg_tuple[2],arg_tuple


class MovableTypeAPI(SimpleItem):
    """Implements the Movable Type API

    See: http://www.movabletype.org/docs/mtmanual_programmatic.html#xmlrpc%20api
    """

    security = ClassSecurityInfo()

    def __init__(self, RPCAuth = None):
        ""
        if RPCAuth:
            self.setupRPCAuth(RPCAuth)

    security.declarePublic('setupRPCAuth')
    def setupRPCAuth(self, RPCAuth):
        RPCAuth.addAuthProvider(authTwoMethods, genericBloggerAuthTwo)

    security.declarePublic('publishPost')
    def publishPost(self, postid, username, password):
        """ Publish a post """
        self.plone_log('mt/publishPost')
        sbtool = getToolByName(self, 'simpleblog_tool')
        post = sbtool.getByUID(postid)        

        if post:
            # do publishing
            wf_tool=getToolByName(self, 'portal_workflow')
            wf_state = wf_tool.getInfoFor(post, 'review_state', '')
            if wf_state != 'published':
                wf_tool.doActionFor(post, 'publish')  # todo
            return XMLRPCTRUE

        raise AttributeError, "Entry %s does not exists" % postid

    security.declarePublic('getRecentPostTitles')
    def getRecentPostTitles(self, blogid, username, password, numberOfPosts=None):
        """Get a list of posts titles by a user.
        The number of posts is unlimited."""
        self.plone_log('mt/getRecentPostTitles')
        sbtool = getToolByName(self, 'simpleblog_tool')
        blog = sbtool.getByUID(blogid)

        brains = blog.getFolderContents(contentFilter={'portal_type': 'BlogEntry'},)
        # todo: what if entries are in subfolders?
        posts = []
        for b in brains:
            entry = b.getObject()
            posts.append( { 'dateCreated':b.created
                            , 'userid':b.Creator
                            , 'postid':entry.UID()
                            , 'title':b.Title
                            , 'description':entry.getBody()
                            , 'mt_excerpt':b.Description
                              })
        if numberOfPosts is not None:
            return posts[:int(numberOfPosts)]

        return posts

    security.declarePublic('getCategoryList')
    def getCategoryList(self, blogid, username, password):
        """ Get a list of available categories """
        self.plone_log('mt/getCategoryList')
        sbtool = getToolByName(self, 'simpleblog_tool')
        blog = sbtool.getByUID(blogid)
        cats = blog.listCategories()
        categories = []
        for cat in cats:
            categories.append(
                {'isPrimary':XMLRPCFALSE, 'categoryId': cat, 'categoryName' : cat})

        return categories

    security.declarePublic('getPostCategories')
    def getPostCategories(self, postid, username, password):
        """ Return an existing posting categories in the RSS format. """
        self.plone_log('mt/getPostCategories')
        sbtool = getToolByName(self, 'simpleblog_tool')
        post = sbtool.getByUID(postid)
        if post:
            cats = post.listCategories()
            res=[]
            for c in cats:
                res.append({'isPrimary':XMLRPCFALSE, 'categoryId':c, 'categoryName':c})
            return res
        else:
            raise AttributeError, "Post %s was not found" % postid

    security.declarePublic('setPostCategories')
    def setPostCategories(self, postid, username, password, categories):
        """ Return an existing posting categories in the RSS format. """
        self.plone_log('mt/setPostCategories')
        sbtool = getToolByName(self, 'simpleblog_tool')
        post = sbtool.getByUID(postid)
        if post:
            res=[]
            categories = [s.get('categoryId', '') for s in categories
                          if s.get('categoryId', '').strip()]
            post.setCategories(categories)
            post.reindexObject()
            return XMLRPCTRUE
        else:
            raise AttributeError, "Post %s was not found" % postid

    security.declarePublic('supportedMethods')
    def supportedMethods(self):
        """Return Value: an array of method names supported by the
        server.
        """
        return [m.split('/')[1] for m in authTwoMethods]

    security.declarePublic('supportedTextFilters')
    def supportedTextFilters(self):
        """Return Value: an array of structs containing String ``key``
        and String ``label``. ``key`` is the unique string identifying
        a text formatting plugin, and ``label`` is the readable
        description to be displayed to a user. ``key`` is the value
        that should be passed in the ``mt_convert_breaks`` parameter
        to newPost and editPost.
        """
        # Not actually valid, but you get the idea
        supported = [{'key':'html',
                      'label':'HTML'},
                     {'key':'stx',
                      'label':'Structured Text'},
                     {'key':'plain-text',
                      'label':'Plain Text'}]
        return supported

    security.declarePublic('getTrackbackPings')
    def getTrackbackPings(self, postid):
        """Return Value: an array of structs containing String
        ``pingTitle`` (the title of the entry sent in the ping),
        String ``pingURL`` (the URL of the entry), and String
        ``pingIP`` (the IP address of the host that sent the ping).
        """
        return []

InitializeClass(MovableTypeAPI)
