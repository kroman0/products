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

