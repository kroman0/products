## Script (Python) "listMetaTags"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Generate Keywords from SEO properties
##

prop_name = 'qSEO_keywords'

if context.hasProperty(prop_name):
    return context.getProperty(prop_name)

accessor = 'Subject'

method = getattr(context, accessor, None)
if not callable(method):
    # ups
    return None

# Catch AttributeErrors raised by some AT applications
try:
    value = method()
except AttributeError:
    value = None

return value
