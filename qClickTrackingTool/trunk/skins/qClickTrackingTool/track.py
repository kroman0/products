from Products.CMFCore.utils import getToolByName
request=container.REQUEST
RESPONSE= request.RESPONSE

path='/'.join(traverse_subpath)
default='/'
map=container.getTrackMap()

if path in map.keys():
    target=map[path]
else:
    target=default

# If the link is absolute, it should be just forwarded
if target.startswith('http://') or \
   target.startswith('https://') or \
   target.startswith('ftp://') :
    return RESPONSE.redirect(target)

# If it starts from root, it just starts from root of portal
root=getToolByName(context, 'portal_url').getPortalObject().absolute_url()
if target.startswith('/'):
    return RESPONSE.redirect(root+target)

# Another option is to try to find the object in the ZODB
target=container.restrictedTraverse(target, None)
if target:
    return RESPONSE.redirect(target.absolute_url())

# Or fallback to root of portal
return RESPONSE.redirect(root)
