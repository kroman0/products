## Controller Python Script "qseo_properties_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##title=Update SEO Properties
##parameters=title=None,description=None,keywords=None,html_comment=None,robots=None,distribution=None,title_override=0,description_override=0,keywords_override=0,html_comment_override=0,robots_override=0,distribution_override=0

def setProperty(context, property, value, type='string'):
    if context.hasProperty(property):
        context.manage_changeProperties({property: value})
    else:
        context.manage_addProperty(property, value, type)

setProperty(context, 'qSEO_title', title)
setProperty(context, 'qSEO_description', description)
setProperty(context, 'qSEO_keywords', keywords, 'lines')
setProperty(context, 'qSEO_html_comment', html_comment)
setProperty(context, 'qSEO_robots', robots)
setProperty(context, 'qSEO_distribution', distribution)

delete_list = []
if not title_override:        delete_list.append('qSEO_title')
if not description_override:  delete_list.append('qSEO_description')
if not keywords_override:     delete_list.append('qSEO_keywords')
if not html_comment_override: delete_list.append('qSEO_html_comment')
if not robots_override:       delete_list.append('qSEO_robots')
if not distribution_override: delete_list.append('qSEO_distribution')

if delete_list: context.manage_delProperties(delete_list)

return state.set(context=context, portal_status_message='Content SEO properties have been saved.')
