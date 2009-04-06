from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.qPloneComments.browser import comments

class CommentsViewlet(comments.CommentsViewlet):
    """A custom version of the comments viewlet
    """
    render = ViewPageTemplateFile('comments.pt')
