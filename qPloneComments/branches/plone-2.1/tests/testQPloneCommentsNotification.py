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
        dm_group = portal_groups.getGroupById(id='DiscussionManager')
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

    
    def testPublishedOFF(self):
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        clearFile(output_file_path('mail.res'))
        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]

        # Set Published Notification OFF
        self.setApprovePublished(swithA=0,swithP=0)
        reply.discussion_publish_comment()
        testNotMail(self)

    def testPublishedON(self):
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        clearFile(output_file_path('mail.res'))
        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]

        # Set Published Notification ON
        self.setApprovePublished(swithA=0,swithP=1)
        reply.discussion_publish_comment()
        testMailSend(self, state='published')


    def testApproveOFF(self):
        # Set Approve Notification OFF
        self.setApprovePublished(swithA=0,swithP=0)
        self.my_doc.discussion_reply('Reply 1', 'text of reply')
        testNotMail(self)


    def testApproveON(self):
        # Set Approve Notification ON
        self.setApprovePublished(swithA=1,swithP=0)
        self.my_doc.discussion_reply('Reply 1', 'text of reply')
        testMailSend(self, state='approve')
    

    def testOFFModerationApprovePublished(self):
        self.prefs._updateProperty('enable_moderation', 0)

        # Test Enable Approve Notification & Enable Published Notification
        self.setApprovePublished(swithA=1, swithP=1)
        self.my_doc.discussion_reply('Reply 1', 'text of reply')
        testMailSend(self, state='approve')
        testMailSend(self, state='published')

    
    def testOFFModerationApprove(self):
        self.prefs._updateProperty('enable_moderation', 0)
        
        # Test Enable Approve Notification & Disable Published Notification
        self.setApprovePublished(swithA=1,swithP=0)
        self.my_doc.discussion_reply('Reply 1', 'text of reply')
        testMailSend(self, state='approve')
        testNotMailSend(self, state='published')


    def testOFFModerationPublished(self): 
        self.prefs._updateProperty('enable_moderation', 0)
        
        # Test Enable Published Notification  & Disable Approve Notification
        self.setApprovePublished(swithA=0,swithP=1)
        self.my_doc.discussion_reply('Reply 1', 'text of reply')
        testNotMailSend(self, state='approve')
        testMailSend(self, state='published')


    def testOFFModeration(self): 
        self.prefs._updateProperty('enable_moderation', 0)
        
        # Test Disable Published Notification & Disable Approve Notification
        self.setApprovePublished(swithA=0,swithP=0)
        self.my_doc.discussion_reply('Reply 1', 'text of reply')
        testNotMailSend(self, state='approve')
        testNotMailSend(self, state='published')
        
    

TESTS = [TestNotification]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNotification))
    return suite

if __name__ == '__main__':
    framework()

