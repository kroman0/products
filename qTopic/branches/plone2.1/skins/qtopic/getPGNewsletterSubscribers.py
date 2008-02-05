##Python Script "getPGNewsletterSubscribers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=newsletter_name=None
##title=
##
members = context

if hasattr(members, 'queryCatalog'):
    return [
        (
            getattr(member, 'getEmail', ''), 
            'HTML', 
            "%s/portal_memberdata/%s/base_edit" % (context.portal_url(), getattr(member, 'id', '')),
        )
        for member in members.queryCatalog()]
else:
    raise "qTopic not found"
