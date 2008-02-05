## Controller Python Script "prefs_simpleblog_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=publishedState='published', createPortletOnBlogCreation=None, maxItemsInPortlet=5, globalCategories=''
##title=Setup SimpleBlog

context.simpleblog_tool.setProperties(publishedState, createPortletOnBlogCreation, maxItemsInPortlet, globalCategories)

return state.set(portal_status_message='SimpleBlog configured.')
