# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
try:
    from Products.qPloneComments.browser import comments
except ImportError:
    from quintagroup.plonecomments.browser import comments

class CommentsViewlet(comments.CommentsViewlet):
    """A custom version of the comments viewlet
    """
    render = ViewPageTemplateFile('comments.pt')
