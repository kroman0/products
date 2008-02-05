from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.viewlets.common import ViewletBase

class TitleCommentViewlet(ViewletBase):

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.page_title = self.context_state.object_title
        self.portal_title = self.portal_state.portal_title

        self.override_title = self.context.hasProperty('qSEO_title')
        self.override_comments = self.context.hasProperty('qSEO_html_comment')

    def render(self):
        std_title = u"<title>%s &mdash; %s</title>" % ( safe_unicode(self.page_title()),
                                                        safe_unicode(self.portal_title())
                                                      )
        if not self.override_title:
            if not self.override_comments:
                return std_title
            else:
                qseo_comments = u"<!--%s-->"%safe_unicode(self.context.qSEO_HTML_Comment())
                return u"%s\n%s"%(std_title, qseo_comments)
        else:
            qseo_title = u"<title>%s</title>" % safe_unicode(self.context.qSEO_Title())
            if not self.override_comments:
                return qseo_title
            else:
                qseo_comments = u"<!--%s-->"%safe_unicode(self.context.qSEO_HTML_Comment())
                return u"%s\n%s"%(qseo_title, qseo_comments)
