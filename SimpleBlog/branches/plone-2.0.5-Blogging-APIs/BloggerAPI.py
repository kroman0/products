#
# Authors: Tom von Schwerdtner <tvon@etria.com>
#          Brian Skahan <bskahan@etria.com>
#
# Copyright 2004, Etria, LLP
#
# This file is part of Quills
#
# Quills is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quills; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.utils import parseHeadersBody 
from AccessControl import ClassSecurityInfo
import DateTime

authOneMethods = [
    'blogger/getTemplate',
    'blogger/setTemplate',
    'blogger/deletePost',
    'blogger/editPost',
    'blogger/newPost',
    'blogger/getRecentPosts'
    ]

def genericBloggerAuthOne(args):
    return args[2],args[3],args


authTwoMethods = [
    'blogger/getUsersBlogs',
    'blogger/getUserInfo'
    ]

def genericBloggerAuthTwo(args):
    return args[1],args[2],args

class BloggerAPI(SimpleItem):
    """http://www.blogger.com/developers/api/1_docs/"""
    security = ClassSecurityInfo()

    def __init__(self, RPCAuth = None):
        ""
        if RPCAuth:
            self.setupRPCAuth(RPCAuth)
        
    security.declarePublic('setupRPCAuth')
    def setupRPCAuth(self, RPCAuth):
        RPCAuth.addAuthProvider(authOneMethods, genericBloggerAuthOne)
        RPCAuth.addAuthProvider(authTwoMethods, genericBloggerAuthTwo)

    security.declarePublic('newPost')
    def newPost(self, appkey, blogid, username, password, content, publish):
        """blogger.newPost makes a new post to a designated blog. Optionally,
        will publish the blog after making the post. On success, it returns the
        unique ID of the new post.  On error, it will return some error
        message."""
        
        self.plone_log('blogger/newPost')

        sbtool = getToolByName(self, 'simpleblog_tool')
        blog = sbtool.getByUID(blogid)

        post = content.split('\n')
        title = post[0]
        if len(title)>25:
            title = str(DateTime.DateTime())
        body = '\n'.join(post[1:])

        #headers, body = parseHeadersBody(content)

        id = sbtool.idFromTitle(title)
        
        self.plone_log("<blogger.newPost()>")
        self.plone_log("blogid: ", blogid)
        self.plone_log("content: ", content)
        #self.plone_log("headers: ", headers)
        #self.plone_log("body: ", body)
        self.plone_log("publish: ", publish)
        self.plone_log("</blogger.newPost()>")
                
        blog.invokeFactory('BlogEntry', id = id, title = title, body = body)
        entry = getattr(blog, id)

        wf_tool = getToolByName(self, 'portal_workflow')
        if publish:
            state = sbtool.getPublishedState()
            entry.setEffectiveDate(DateTime.DateTime())
            
            # todo xxxxxxxxxx
            wf_tool.doActionFor(entry,'publish', None)

        return entry.UID()

    security.declarePublic('editPost')
    def editPost(self, appkey, postid, username, password, content, publish):
        """blogger.editPost changes the contents of a given post. Optionally,
        will publish the blog the post belongs to after changing the post. On
        success, it returns a boolean true value. On error, it will return a
        fault with an error message."""
        self.plone_log('blogger/editPost')

        sbtool = getToolByName(self, 'simpleblog_tool')
        
        entry = sbtool.getByUID(postid)
        
        entry.setBody(content, mimetype='text/html')
        
        if publish:
            wf_tool = getToolByName(self, 'portal_workflow')
            entry.setEffectiveDate(DateTime.DateTime())
            wf_tool.doActionFor(entry, 'publish', None)
            
        return True

    security.declarePublic('deletePost')
    def deletePost(self, appkey, postid, username, password, publish):
        "Returns true on success, fault on failure"
        self.plone_log('blogger/deletePost')

        sbtool = getToolByName(self, 'simpleblog_tool')
        
        entry = sbtool.getByUID(postid)

        entry.aq_inner.aq_parent.manage_delObjects(entry.getId())

        return True
        
    security.declarePublic('getRecentPosts')
    def getRecentPosts(self, appkey, blogid, username, password, num):
        "Return 'num' recent posts to specified blog"
        self.plone_log('blogger/getRecentPosts')
        sbtool = getToolByName(self, 'simpleblog_tool')
        blog = sbtool.getByUID(blogid)
        entries = blog.getFolderListingFolderContents(contentFilter={'portal_type': 'BlogEntry'},)

        posts = []
        for entry in entries:
            posts.append( { 'dateCreated':entry.created()
                            , 'userid':entry.Creator()
                            , 'postid':entry.UID()
                            , 'title':entry.Title()
                            , 'description':entry.getBody()
                            , 'excerpt':entry.Description()
                            , 'content':entry.getBody()
                              })    
        
        
        if num is not None:
            return posts[:int(num)]
        return posts
    
        
    security.declarePublic('getUsersBlogs')
    def getUsersBlogs(self, appkey, username, password):
        """blogger.getUsersBlogs returns information about all the blogs a
        given user is a member of. Data is returned as an array of <struct>'s
        containing the ID (blogid), name (blogName), and URL (url) of each
        blog."""
        self.plone_log('blogger/getUsersBlogs')
        catalog = getToolByName(self, 'portal_catalog')
        results = catalog(meta_type='Blog')

        blogs = []
        for item in results:
            o = item.getObject()
            if o.portal_membership.checkPermission('Modify portal content', o):
                blogs.append(
                        {'url': o.absolute_url(),
                         'blogid' : o.UID(),
                         'blogName' : o.title_or_id()}
                        )

        return blogs

    security.declarePublic('getUserInfo')
    def getUserInfo(self, appkey, username, password):
        """blogger.getUserInfo returns returns a struct containing user's
        userid, firstname, lastname, nickname, email, and url."""
        self.plone_log('blogger/getUserInfo')

        membership=getToolByName(self, 'portal_membership')
        info={'name':'no name','email':'no email','userid':'no user id'
               ,'firstname':'no first name','lastname':'no last name'
               ,'url':'no url'}
        member=membership.getAuthenticatedMember()
        if member:
            for key,value in info.items():
                info[key] = getattr(member,key,None) or value
        return info

    security.declarePublic('getTemplate')
    def getTemplate(self):
        """blogger.getTemplate returns text of the main or archive index
        template for a given blog."""
        # Not implementing
        self.plone_log('blogger/getTemplate')
        pass

    security.declarePublic('setTemplate')
    def setTemplate(self):
        """blogger.setTemplate changes the template for a given blog. Can
        change either main or archive index template."""
        # Not implementing
        self.plone_log('blogger/setTemplate')
        pass

