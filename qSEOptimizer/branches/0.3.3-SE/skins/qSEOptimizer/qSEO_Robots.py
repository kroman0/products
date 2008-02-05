## Script (Python) "qSEO_Description"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Generate Description from SEO properties
##

prop_name = 'qSEO_robots'

if context.hasProperty(prop_name):
    return context.getProperty(prop_name)

# by default make robots crawl website
return 'ALL'
