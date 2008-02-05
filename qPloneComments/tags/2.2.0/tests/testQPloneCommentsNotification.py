#
# Test configuration form working
#

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal, ReplyToItem
from Products.MailHost.MailHost import MailBase
from helperNotify import *

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


TESTS = [TestNotification]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNotification))
    return suite

if __name__ == '__main__':
    framework()

