##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters = product, docformat = 'restructuredtext', css = 'white'
##title=
##
request=context.REQUEST
portal_doc = context.portal_documentation
try:
    portal_doc.generate(product, docformat = docformat, css = css)
    return state.set(status='success', portal_status_message='%s documentation generated successfuly' % product)
except:
    return state.set(status='failure', portal_status_message='Internal Error #occured in epydoc')
