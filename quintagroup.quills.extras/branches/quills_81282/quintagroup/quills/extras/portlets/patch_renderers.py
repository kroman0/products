from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from quills.app.portlets.authors import Renderer as AuthorBaseRenderer
from quills.app.portlets.recentcomments import Renderer as RecentCommentsBaseRenderer
from quills.app.portlets.recententries import Renderer as RecentEntriesBaseRenderer


class AuthorRenderer(AuthorBaseRenderer):

    _template = ViewPageTemplateFile('authors.pt')

class RecentCommentsRenderer(RecentCommentsBaseRenderer):

    _template = ViewPageTemplateFile('recentcomments.pt')

class RecentEntriesRenderer(RecentEntriesBaseRenderer):

    _template = ViewPageTemplateFile('weblogrecententries.pt')

