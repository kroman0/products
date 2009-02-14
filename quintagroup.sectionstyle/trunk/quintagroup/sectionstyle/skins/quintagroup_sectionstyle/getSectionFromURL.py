## Script (Python) "getSectionFromURL"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Returns section name (first part of URL) to the body tag and looks for context properties
##
html_class = ''

from Products.CMFCore.utils import getToolByName

portal_url = getToolByName(context, 'portal_url')
contentPath = portal_url.getRelativeContentPath(context)
if contentPath:
    html_class += "section-%s" % contentPath[0]

# add html class taken from context's property called 'body_class'
if context.hasProperty('body_class'):
    value = context.getProperty('body_class')
    if html_class:
        html_class += ' %s' % value
    else:
        html_class = value

return html_class
