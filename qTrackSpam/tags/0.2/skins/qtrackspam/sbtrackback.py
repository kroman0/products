## Script (Python) "trackback"   
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=url='',title='',excerpt='',blog_name=''
##title=Provide trackback functionality
##
from DateTime import DateTime
from Products.SimpleBlog.util import addTrackBack

request = context.REQUEST
if not hasattr(request, 'url'):
    print context.sbtrackbackResponse(code=0,msg="URL is missing")
    return printed

   
#url = request.get('url','')
#title = request.get('title', '')
#excerpt = request.get('excerpt', '') 
#blog_name = request.get('blog_name', '')

url = request.get('url', url)
title = request.get('title', title)
excerpt = request.get('excerpt', excerpt) 
blog_name = request.get('blog_name', blog_name)

# Check for spam
trackspam = context.portal_trackspam
if not trackspam.checkURL(url):
    print context.sbtrackbackResponse(code=0, msg="Identified as SPAM")
    return printed

ids=context.objectIds()
id=0

now=DateTime()
id=now.strftime('%Y%m%d')+now.strftime('%M%S')


try:
	context.invokeFactory(id=id, type_name='TrackBack')
	trback = getattr(context, id, None)
	trback.setUrl(url)
	trback.setTitle(title)
	trback.setBlog_name(blog_name)
	trback.setExcerpt(excerpt)
except:
	print context.sbtrackbackResponse(code=0, msg="") 
	return printed
return context.sbtrackbackResponse(code=1, msg="ok") 
