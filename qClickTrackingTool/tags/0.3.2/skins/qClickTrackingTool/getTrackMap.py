from Products.CMFCore.utils import getToolByName

portal_clicktracker=getToolByName(context, 'portal_clicktracker')
links=portal_clicktracker.listFolderContents()
track_map={}
for link in links:
    track_map[link.getId()]=link.getRemoteUrl()

return track_map