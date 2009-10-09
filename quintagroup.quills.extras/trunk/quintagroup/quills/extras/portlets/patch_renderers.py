# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from quills.app.portlets.authors import Renderer as AuthorBaseRenderer
from quills.app.portlets.recentcomments import Renderer as RecentCommentsBaseRenderer
from quills.app.portlets.recententries import Renderer as RecentEntriesBaseRenderer
from quills.app.portlets.quillslinks import Renderer as QuillsLinksBaseRenderer


class AuthorRenderer(AuthorBaseRenderer):

    _template = ViewPageTemplateFile('authors.pt')

class RecentCommentsRenderer(RecentCommentsBaseRenderer):

    _template = ViewPageTemplateFile('recentcomments.pt')

    @property
    def getComments(self):
        weblog_content = self.getWeblogContentObject()
        if weblog_content is None:
            return []

        context = self.context.aq_inner
        pc = getToolByName(context, 'portal_catalog')
        comment_brains = pc({
            'portal_type' : 'Discussion Item', 
            'sort_on' : 'modified', 
            'sort_order' : 'reverse',
            'path' : {'query' : '/'.join(context.getPhysicalPath()),}
             })
        return comment_brains[:self.data.max_comments]

class RecentEntriesRenderer(RecentEntriesBaseRenderer):

    _template = ViewPageTemplateFile('weblogrecententries.pt')

class QuillsLinksRenderer(QuillsLinksBaseRenderer):

    _template = ViewPageTemplateFile('quillslinks.pt')
