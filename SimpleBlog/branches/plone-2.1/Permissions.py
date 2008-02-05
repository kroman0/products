from Products.CMFCore.CMFCorePermissions import setDefaultRoles

# Add Entry
ADD_BLOGENTRY_PERMISSION = 'SimpleBlog: Add BlogEntry'
ADD_SIMPLEBLOG_PERMISSION='SimpleBlog: Add Blog'

setDefaultRoles(ADD_BLOGENTRY_PERMISSION, ( 'Manager', 'Owner' ) )

