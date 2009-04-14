## Script (Python) "qSEO_ECMA_Script"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Generate ECMA Script from SEO properties
##

prop_name = 'qSEO_ecma_script'

if context.hasProperty(prop_name):
    return context.getProperty(prop_name)

# No ecma script by default
return ''
