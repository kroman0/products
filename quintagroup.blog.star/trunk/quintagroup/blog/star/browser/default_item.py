from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
import re

START_RE = re.compile('<h1[^<>]+documentFirstHeading[^<>]+>') # Standard plone header
END_RE = re.compile('</h1>')

RELTAG_RE = re.compile("<a[^<>]*rel=\"tag\"[^<>]*>", re.S)
HREF_RE = re.compile("href=\"([^\?]*)\?", re.S)

class DefaultItemView(BrowserView):
    """
    The default blog item view
    """
    
    template = ViewPageTemplateFile("default_item.pt")
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self, blog=None):
        html = self.template()
        tag = START_RE.search(html)
        if not tag:
            return html
        startpos = tag.end()
        endpos = END_RE.search(html, startpos).start()

        portal_properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        use_view = site_properties.getProperty('typesUseViewActionInListings')
        if self.context.portal_type in use_view:
            postfix = '/view'
        else:
            postfix = ''

        # Fix field under
        if blog:
            reltags = RELTAG_RE.findall(html)
            repl_url = 'href="%s?' % blog.absolute_url()
            for src_tag in reltags:
                res_tag = HREF_RE.sub(repl_url, src_tag)
                html = html.replace(src_tag, res_tag)

        result = (html[:startpos],
                  '<a href="',
                  self.context.absolute_url(),
                  postfix,
                  '">',
                  html[startpos:endpos],
                  '</a>',
                  html[endpos:])
        return ''.join(result)

        
