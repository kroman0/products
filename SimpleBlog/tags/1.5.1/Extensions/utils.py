def notifyTrackBack(change_state=None):
    if not change_state:
        return None
    obj = change_state.object
    portal = change_state.getPortal()
    # Get Blog object
    blog = obj
    while 1:
        if blog.meta_type == 'Blog':
            break
        blog = blog.aq_parent

    to_email = blog.getAdminEmail()
    from_email = portal.getProperty("email_from_address", "postmaster@localhost")
    if to_email:
        # get additional data for mail-template
        post_title = obj.aq_parent.Title()
        obj_url = obj.absolute_url()
        charset = portal.portal_properties.site_properties.getProperty('default_charset','utf-8')
        body = obj.notifyTBtemplate(from_email=from_email, \
                                    to_email=to_email, \
                                    charset=charset, \
                                    post_title=post_title, \
                                    obj_url=obj_url)
        try:
            mh = portal.MailHost
            mh.send(body)
        except:
            pass


from Products.SimpleBlog import MetaWeblogAPI
from Products.SimpleBlog import BloggerAPI
from Products.SimpleBlog import MovableTypeAPI

def migrateToAPIs(self):
    """ migrate existing SimpleBlog instance to support BloggingAPIs """
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
