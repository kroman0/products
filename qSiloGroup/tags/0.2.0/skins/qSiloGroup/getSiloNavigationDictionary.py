## Controller Python Script "getSiloNavigationDictionary"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Update Folder Property
##parameters=
#

from Products.CMFCore.utils import getToolByName

if context.portal_type in ['Folder', 'Large Plone Folder', 'CMFFolder']: CONTEXT = context
else: CONTEXT = context.aq_parent

items = CONTEXT.getProperty('silo_items',None)

if not items:
    return {}

links = getToolByName(context, 'portal_catalog').searchResults(path="/".join(CONTEXT.getPhysicalPath()), portal_type="Link")
links_dict = {}
for l in links:
    links_dict[l.getId] = l.getRemoteUrl

prop_dict = {}
for i in items:
    s = map(str, i.split('|'))
    id = s[0]
    path = id
    link = False
    try:
        if len(s) == 2:
            title = s[1]
        else:
            title = s[2]
            path += s[1] and ('/'+s[1]) or s[1]
        if id in links_dict.keys():
            link = True
            path = links_dict[id]
        prop_dict[id] = {'id': id, 'path':path, 'title':title, 'link':link}
    except: continue

return prop_dict