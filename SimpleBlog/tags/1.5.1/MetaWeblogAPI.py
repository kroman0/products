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
from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager, newSecurityManager

import DateTime
import re
import xmlrpclib
import random

authMethods = [
    'metaWeblog/getPost',
    'metaWeblog/deletePost',
    'metaWeblog/editPost',
    'metaWeblog/newPost',
    'metaWeblog/getRecentPosts',
    'metaWeblog/getUsersBlogs',
    'metaWeblog/getCategories',
    'metaWeblog/newMediaObject'
    ]

def genericMetaWeblogAuth(args):
    return args[1], args[2], args


class MetaWeblogAPI(SimpleItem):
    """http://www.metaWeblog.com/developers/api/1_docs/"""
    security = ClassSecurityInfo()

    def __init__(self, RPCAuth = None):
        ""
        if RPCAuth:
            self.setupRPCAuth(RPCAuth)
        
    security.declarePublic('setupRPCAuth')
    def setupRPCAuth(self, RPCAuth):
        RPCAuth.addAuthProvider(authMethods, genericMetaWeblogAuth)

    security.declarePublic('newPost')
    def newPost(self, blogid, username, password, struct, publish):
        """Some Stuff"""
        
        self.plone_log('metaWeblog/newPost')
        print 'metaWeblog/newPost'
        
        sbtool = getToolByName(self, 'simpleblog_tool')

        blog = sbtool.getByUID(blogid)

        body  = struct.get('description', struct.get('Description'))
        title = struct.get('title', struct.get('Title'))
        description = struct.get('mt_excerpt', '')
        allow_comments = struct.get('mt_allow_comments', 1)
        
        id = sbtool.idFromTitle(title)

        blog.invokeFactory('BlogEntry', id = id, title = title)
        entry = getattr(blog, id)

        entry.setBody(body, mimetype='text/html')
        entry.setDescription(description)

        # The workflow moves the entry, so get the UID now
        entry_uid = entry.UID()

        wf_tool = getToolByName(self, 'portal_workflow')
        if publish:
            state = sbtool.getPublishedState()
            entry.setEffectiveDate(DateTime.DateTime())
            
            # todo xxxxxxxxxx
            wf_tool.doActionFor(entry, 'publish', None)

        return entry_uid

    security.declarePublic('editPost')
    def editPost(self, postid, username, password, struct, publish):
        """Some stuff"""
        self.plone_log('metaWeblog/editPost')
        print 'metaWeblog/editPost'
        sbtool = getToolByName(self, 'simpleblog_tool')
        
        entry = sbtool.getByUID(postid)

        body  = struct.get('description', struct.get('Description'))    
        title = struct.get('title', struct.get('Title'))
        description = struct.get('mt_excerpt', '')
        allow_comments = struct.get('mt_allow_comments', 1)
        
        entry.setBody(body, mimetype='text/html')
        entry.setTitle(title)
        entry.setDescription(description)
        disc_tool = getToolByName(self, 'portal_discussion')
        
        #if allow_comments:
            #disc_tool.overrideDiscussionFor(entry, 1)
        #else:
            #disc_tool.overrideDiscussionFor(entry, 0)
 
        #  portal.portal_workflow.getInfoFor(here,'review_state',None)   (from folder_contents.pt)
        wf_tool=getToolByName(self, 'portal_workflow')
        wf_state = wf_tool.getInfoFor(entry, 'review_state', '')
        if publish and wf_state != 'published':  # todo!!!!
            wf_tool.doActionFor(entry, 'publish')

        entry.reindexObject()
                    
        return True
        
    security.declarePublic('getPost')
    def getPost(self, postid, username, password):
        "Return a post I suppose"
        self.plone_log('metaWeblog/getPost')
        print 'metaWeblog/getPost'
        sbtool = getToolByName(self, 'simpleblog_tool')
        
        post = sbtool.getByUID(postid)
        disc_tool = getToolByName(self, 'portal_discussion')
        res = {}
        if post:
            res['postid'] = post.UID()
            res['title'] = post.Title()
            res['link'] = post.absolute_url()
            res['category'] = post.listCategories()
            res['categories'] = post.listCategories()
            res['description'] = post.getBody()
            res['mt_excerpt'] = post.Description()
            res['mt_text_more']=post.getBody()
            res['mt_allow_comments']=disc_tool.isDiscussionAllowedFor(post)
                
            return res
        else:
            raise AttributeError, "Post %s was not found" % postid

        return res
        
    security.declarePublic('getCategories')
    def getCategories(self, blogid, username, password):
        "Returns a struct containing description, htmlUrl and rssUrl"
        self.plone_log('metaWeblog/getCategories')
        print 'metaWeblog/getCategories'
        sbtool = getToolByName(self, 'simpleblog_tool')
        
        blog = sbtool.getByUID(blogid)
        
        cats = blog.listCategories()
        
        categories = []
        for cat in cats:
            categories.append(
                {'categoryName': cat, 'description' : cat,
                'htmlUrl' : blog.absolute_url() + ',/SimpleBlogCatSearch?category=' + cat,
                'rssUrl' : blog.absolute_url() + ',/SimpleBlogCatSearch?category=' + cat
                })
                
        self.plone_log('metaWeblog/getCategories: returning ', categories)
        return categories

    security.declarePublic('deletePost')
    def deletePost(self, postid, username, password, publish):
        "Returns true on success, fault on failure"
        self.plone_log('metaWeblog/deletePost')
        print 'metaWeblog/deletePost'
        sbtool = getToolByName(self, 'simpleblog_tool')
        
        entry = sbtool.getByUID(postid)

        entry.aq_inner.aq_parent.manage_delObjects(entry.getId())

        return True

    security.declarePublic('getRecentPosts')
    def getRecentPosts(self, blogid, username, password, num):
        """Return 'num' recent posts to specified blog, returns a struct: 
         The three basic elements are title, link and description. 
         For blogging tools that don't support titles and links, the description element holds what the Blogger API refers to as 'content'."""

        self.plone_log('metaWeblog/getRecentPosts')
        print 'metaWeblog/getRecentPosts'
        sbtool = getToolByName(self, 'simpleblog_tool')
        blog = sbtool.getByUID(blogid)

        entries = blog.getFolderListingFolderContents(contentFilter={'portal_type': 'BlogEntry'},)        
        # todo: what if entries are in subfolders?
        
        posts = []
        for entry in entries:
            posts.append( { 'dateCreated':entry.created()
                            , 'userid':entry.Creator()
                            , 'postid':entry.UID()
                            , 'title':entry.Title()
                            , 'description':entry.getBody()
                            , 'excerpt':entry.Description()
                              })            
            
        if num is not None:
            return posts[:int(num)]
        return posts
    
    security.declarePublic('getUsersBlogs')
    def getUsersBlogs(self, username, password):
        """ Return all the blogs the user has access and write permission to """

        self.plone_log('metaWeblog/getUsersBlogs')
        print 'metaWeblog/getUsersBlogs'
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
        """metaWeblog.getUserInfo returns a struct containing user's
        userid, firstname, lastname, nickname, email, and url."""
        self.plone_log('metaWeblog/getUserInfo')
        print 'metaWeblog/getUserInfo'

        membership=getToolByName(self, 'portal_membership')
        info={'name':'no name','email':'no email','userid':'no user id'
               ,'firstname':'no first name','lastname':'no last name'
               ,'url':'no url'}
        member=membership.getAuthenticatedMember()
        if member:
            for key,value in info.items():
                info[key] = getattr(member,key,None) or value
        return info


    security.declarePublic('newMediaObject')
    def newMediaObject(self, blogid, username, password, struct):
        """Create media object and return it's URL or exception"""
        
        self.plone_log('metaWeblog/newMediaObject')
        print 'metaWeblog/newMediaObject'
        
        sbtool = getToolByName(self, 'simpleblog_tool')
        blog = sbtool.getByUID(blogid)
        
        media_name = struct.get('name', None)
        mime_type = struct.get('type', None)
        data = struct.get('bits', '')

        if not media_name or media_name.startswith('.'):
            raise AttributeError, "No 'name' of media object supply or starts with '.'"
        if not mime_type:
            raise AttributeError, "No 'type' of media object supply"
        if not (mime_type.startswith('image') or mime_type.startswith('application')):
            raise AttributeError, "'%s' - not supported mime tipe." % mime_type

        if not 'images' in blog.objectIds():
            blog.invokeFactory('BlogFolder', id = 'images', title='Container for images')
            images = getattr(blog, 'images')
        else:
            images = blog.images

        id = re.sub('[^A-Za-z0-9_.]', '', re.sub(' ', '_', media_name)).lower()
        while id in images.objectIds():
            index = id.rfind('.')
            if index > -1:
                front = id[:index]
                ext = id[index:]
            else:
                front = id
                ext = ''
            id = front + str(random.randint(1,100)) + ext

        images.invokeFactory('Image', id=id, title=media_name, file=str(data)) 
        image = getattr(images, id)

        return {'url':image.absolute_url()}
