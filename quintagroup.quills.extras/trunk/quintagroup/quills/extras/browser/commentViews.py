from quills.app.browser.controllerView import FormControllerView, getToolByName
from quills.app.utilities import talkbackURL
from plone.memoize import instance
from plone.app.content.browser.tableview import Table
from zope.component import getMultiAdapter
from zope.interface import implements
import urllib, re


talkback_url_extractor = re.compile("(.*)/talkback/\d+")

class ManageCommentsView(FormControllerView):
    """ The view class for the comments management form """
    
    def __init__(self, context, request):
        super(ManageCommentsView, self).__init__(context, request)

        self.form_submitted = bool(request.get('form.submitted'))
        if bool(request.get('form.button.Delete')):
            self.mode = "delete"
        elif bool(request.get('form.button.Update')):
            self.mode = "update"
        elif bool(request.get('form.button.ResetFilter')):
            self.mode = "reset"
        elif bool(request.get('form.button.Publish')):
            self.mode = "publish"
        else:
            self.mode = 'display'

        self.author = request.get('form.field.author', '')
        self.subject = request.get('form.field.subject', '')
        self.review_state = request.get('form.field.review_state', '')
        self.selected_comments = request.get('selected_comments', [])
        self.portal_catalog = getToolByName(self.context,'portal_catalog')

        self.contentFilter = {
            'portal_type' : 'Discussion Item', 
            'sort_on' : 'created', 
            'sort_order' : 'reverse',
            'path' : {'query' : '/'.join(self.context.getPhysicalPath()),}
        }

        self.filtered = False
        if self.mode in ['delete', 'display', 'update']:
            if self.author:
                self.contentFilter['Creator'] = self.author
                self.filtered = True
            if self.subject:
                self.contentFilter['Title'] = self.subject
                self.filtered = True
            if not self.review_state and self.contentFilter.has_key('review_state'):
                del self.contentFilter['review_state']
                self.filtered = True
            elif self.review_state in ['published', 'private']:
                self.contentFilter['review_state'] = self.review_state
                self.filtered = True
	        
        if self.mode == "display":
            self.getComments()

    def validate(self):
        """ performs validation and returns an errors dictionary """
        errors = {}
        if self.mode=='delete':
            if self.selected_comments == []:
                errors['status'] = 'failure'    # errors must not be empty...            
                self.setMessage('You must select at least one comment for deletion.')
                self.getComments()
        return errors

    def control(self):
        """ performs the actions after a successful validation possibly
            returning an errors dictionary """

        if self.mode == "update":
            self.setMessage('Filter applied.')
        elif self.mode == "reset":
            self.setMessage('Filter reset.')
            self.author = None
            self.subject = None
            self.review_state = None
        elif self.mode == "delete":
            discussion_tool = getToolByName(self.context, 'portal_discussion')
            for path in self.selected_comments:
                self.deleteReply(discussion_tool, self.portal_catalog, path)
            self.setMessage('%s comments have been deleted.' % str(len(self.selected_comments)))
        elif self.mode == 'publish':
            for path in self.selected_comments:
                self.publishReply(self.portal_catalog, path)
            self.setMessage('%s comments have been published.' % str(len(self.selected_comments)))
        self.getComments()
        return {}
            
    def deleteReply(self, dtool, pcatalog, path):
        discussion_item = pcatalog(path=path)[0].getObject()
        obj = discussion_item.parentsInThread()[0]
        discussion = dtool.getDiscussionFor(obj)
        discussion.deleteReply(discussion_item.getId())

    def publishReply(self, pcatalog, path):
        """publish the discussion item"""
        discussion_item = pcatalog(path=path)[0].getObject()
        roles = ['Anonymous']
        discussion_item.review_state = "published"
        discussion_item.manage_permission('View', roles, acquire=1)
        discussion_item._p_changed = 1
        discussion_item.reindexObject()
	
    def getComments(self):
        self.comment_brains = self.portal_catalog(self.contentFilter)
        self.num_of_comments = len(self.comment_brains)
        self.has_comments = self.num_of_comments > 0
        #return self.comment_brains
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_view = getMultiAdapter((self.context, self.request), name=u'plone')
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        portal_properties = getToolByName(self.context, 'portal_properties')

        curl = self.context.absolute_url()
        results = []
        for i, obj in enumerate(self.comment_brains):
            if (i + 1) % 2 == 0:
                table_row_class = "draggable even"
            else:
                table_row_class = "draggable odd"
            
            url = obj.getURL()
            path = obj.getPath or "/".join(obj.getPhysicalPath())
            absolute_url = url[:url.find('/talkback')]
            url = "%s#%s" % (absolute_url, obj.id)
            icon = None
            
            review_state = obj.review_state
            state_class = 'state-' + plone_utils.normalizeString(review_state)
            relative_url = obj.getURL(relative=True)
            obj_type = obj.portal_type
            modified = plone_view.toLocalizedTime(
                obj.ModificationDate, long_format=1)
            view_url = url
            results.append(dict(
                url = url,
                Creator = obj.Creator,
                id  = obj.getId,
                quoted_id = obj.getId,
                path = path,
                title_or_id = obj.Title,
                description = obj.Description,
                obj_type = obj_type,
                size = obj.getObjSize,
                modified = modified,
                icon = '',
                type_class = 'contenttype-discutionitem',
                wf_state = review_state,
                state_title = review_state,
                state_class = state_class,
                is_browser_default = 0,
                folderish = 0,
                relative_url = relative_url,
                view_url = view_url,
                table_row_class = table_row_class,
                is_expired = 0,
                ))
        self.table = Table(self.request, curl, curl+'/manage_comments', results)
        return self.comment_brains
        
        
    def talkbackURL(self, item):
        return talkbackURL(item)
