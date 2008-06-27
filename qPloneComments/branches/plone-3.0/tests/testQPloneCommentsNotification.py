#
# Test configuration form working
#

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal, ReplyToItem

import re
from helperNotify import *
from Products.qPloneComments.utils import getMsg

PRODUCT = 'qPloneComments'
PROPERTY_SHEET = "qPloneComments"

PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite()


class TestNotification(PloneTestCase.FunctionalTestCase):

    def setApprovePublished(self, swithA=1,swithP=1):
        self.prefs._updateProperty('enable_approve_notification', swithA)
        self.prefs._updateProperty('enable_published_notification', swithP)

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(PRODUCT)
        # VERY IMPORTANT to guarantee product skin's content visibility
        self._refreshSkinData()

        '''Preparation for functional testing'''
        self.discussion = getToolByName(self.portal, 'portal_discussion', None)
        # Allow discussion for Document
        portal_types = getToolByName(self.portal, 'portal_types', None)
        doc_fti = portal_types.getTypeInfo('Document')
        doc_fti._updateProperty('allow_discussion', 1)

        # Make sure Documents are visible by default
        # XXX only do this for plone 3
        self.portal.portal_workflow.setChainForPortalTypes(('Document',), 'plone_workflow')

        portal_properties = getToolByName(self.portal, 'portal_properties', None)
        self.prefs = portal_properties[PROPERTY_SHEET]

        # Add Manager user - 'dm' and add him to Discussion Manager group
        self.portal.portal_membership.addMember('dm', 'secret' , ['Manager'], [])
        portal_groups = getToolByName(self.portal, 'portal_groups')
        dm_group = portal_groups.getGroupById('DiscussionManager')
        dm_group.addMember('dm')
        self.logout()
        self.login('dm')
        # For prepare mail sending - enter an e-mail adress
        self.prefs._updateProperty('email_discussion_manager', 'discussion.manager@test.com')
        member = self.portal.portal_membership.getAuthenticatedMember()
        member.setMemberProperties({'email':'creator@test.com'})

        # Add testing document to portal
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')
        # Create talkback for document and Prepare REQUEST
        self.discussion.getDiscussionFor(self.my_doc)
        self.request = self.app.REQUEST
        self.request.form['Creator'] = self.portal.portal_membership.getAuthenticatedMember().getUserName()
        self.request.form['subject'] = "Reply 1"
        self.request.form['body_text'] = "text of reply"

        prepareMailSendTest()

    def test_bug_parent_reply(self):
        setProperties(self.prefs, 'enable_reply_user_notification')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        parent_reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        parent_reply.discussion_reply('reply', 'text')

    def test_bug_mistakable_names(self):
        setProperties(self.prefs, 'enable_reply_user_notification')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        parent_reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]

        args={'mto': 'user_email@gmail.com',
              'mfrom': 'admin_email@gmail.com',
              'obj': parent_reply,
              'organization_name': 'org_name',
              'name': parent_reply.getOwnerTuple()[1]}

        msg = getMsg(self.portal, 'reply_notify_template', args)
        patt = re.compile('\\n\\n([^,]*)')
        m = patt.search(msg)
        if m:
            name = m.group(1)
            self.assertEqual(parent_reply.getOwnerTuple()[1], name)
        else:
            raise "No name"

    def test_notificafion_disabled(self):
        cleanOutputDir()
        setProperties(self.prefs)
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.assert_(not testMailExistance(), 'Mail was sended when all notification was disabled')

    def test_published_comment_notification(self):
        cleanOutputDir()
        setProperties(self.prefs, 'enable_published_notification')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.assert_(testMailExistance(), 'Mail was not sended when enable_published_notification')

    def test_approve_comment_notification(self):
        cleanOutputDir()
        setProperties(self.prefs, 'enable_approve_notification')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.assert_(testMailExistance(), 'Mail was not sended when enable_approve_notification')

    def test_reply_comment_user_notification(self):
        cleanOutputDir()
        setProperties(self.prefs, 'enable_reply_user_notification')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.assert_(not testMailExistance(), 'Mail was sended for simple reply when enable_reply_user_notification')

        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        reply.discussion_reply('A Reply for comment' ,'text of reply for comment')
        reply_for_comment = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        self.assert_(testMailExistance(), 'Mail was not sended when enable_reply_user_notification')

    def test_rejected_comment_notification(self):
        cleanOutputDir()
        setProperties(self.prefs, 'enable_rejected_user_notification', 'enable_moderation')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.assert_(not testMailExistance(), 'Mail was sended when enable_rejected_user_notification was enabled')

        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        self.portal.REQUEST.set('ids', [reply.getId()])
        self.portal.prefs_recent_comments_delete()
        self.assert_(testMailExistance(), 'Mail was not sended when enable_rejected_user_notification')

    def test_approve_comment_user__notification(self):
        cleanOutputDir()
        setProperties(self.prefs, 'enable_approve_user_notification')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.assert_(testMailExistance(), 'Mail was not sended when enable_approve_user_notification')

    def test_bug_notification_on_single_reply_publish(self):
        """ Bug: no notification sent on publishing single comment.
            Must be 3 mails: for replier about replying on his commen;
                             for replier about publishig his comment;
                             for document creator about adding new comment.
        """
        properties = ['enable_approve_user_notification', 'enable_reply_user_notification',
                      'enable_published_notification']
        setProperties(self.prefs, *properties)
        #setProperties(self.prefs, 'enable_published_notification', )
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        reply.discussion_reply('A Reply for reply for my_doc' ,'text of reply on reply for my_doc')
        reply2 = self.discussion.getDiscussionFor(reply).getReplies()[0]

        cleanOutputDir()
        reply2.discussion_publish_comment()
        mails = getMails()
        self.assert_([1 for m in mails if re.search('^Subject:.*(replied).*$', m, re.I|re.M)] \
                     ,'No notification for reply' % properties)
        self.assert_([1 for m in mails if re.search('^Subject:.*(added).*$', m, re.I|re.M)] \
                     , 'No notification for adding comment' % properties)
        self.assert_([1 for m in mails if re.search('^Subject:.*(published).*$', m, re.I|re.M)] \
                     , 'No notification for publishing comment' % properties)

    def test_bug_notification_on_single_reply_delete(self):
        """ Bug: no notification sent on deleting single comment.
            Mail about rejecing comment should be sent to comentator.
        """
        properties = ['enable_rejected_user_notification',]
        setProperties(self.prefs, *properties)
        #setProperties(self.prefs, 'enable_published_notification', )
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]

        cleanOutputDir()
        reply.deleteDiscussion()
        mails = getMails()
        self.assert_([1 for m in mails if re.search('^Subject:.*(not approved).*$', m, re.I|re.M)] \
                     ,'No notification for rejecting comment' % properties)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNotification))
    return suite
