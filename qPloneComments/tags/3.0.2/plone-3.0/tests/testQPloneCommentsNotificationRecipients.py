#   
# Test configuration form working
#

import os, sys, string

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFCore.permissions import ManagePortal, ReplyToItem
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ManagePortal,ReplyToItem
from Products.MailHost.MailHost import MailBase

import re

from Products.qPloneComments.utils import getMsg
from testQPloneCommentsModeration import USERS, COMMON_USERS_IDS, DM_USERS_IDS
from helperNotify import *
from common import *

PRODUCT = 'qPloneComments'
PROPERTY_SHEET = "qPloneComments"

PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite()

USERS = {# Common Members
         'admin':{'passw': 'secret_admin', 'roles': ['Manager']},
         'owner':{'passw': 'secret_creator', 'roles': ['Member']},
         'replier1':{'passw': 'secret_member', 'roles': ['Member']},
         'replier2':{'passw': 'secret_member', 'roles': ['Member']},
         # Members for discussion manager group
         'dm_admin':{'passw': 'secret_dm_admin', 'roles': ['Manager']},
        }
DM_USERS_IDS = [u for u in USERS.keys() if u.startswith('dm_')]

REXP_TO = re.compile("To:\s*(.*?)$",re.M)
REXP_SUBJ = re.compile("Subject:\s*(.*?)$",re.M)

class TestNotificationRecipients(PloneTestCase.FunctionalTestCase):
    """ Test is notifications sends to right recipients. """

    def prepareRequest4Reply(self, member_id):
        self.login(member_id)
        self.request = self.app.REQUEST
        self.request.form['Creator'] = self.membership.getAuthenticatedMember().getUserName()
        self.request.form['subject'] = "Reply of '%s'" % self.request.form['Creator']
        self.request.form['body_text'] = "text of reply"


    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(PRODUCT)
        # VERY IMPORTANT to guarantee product skin's content visibility
        self._refreshSkinData()

        '''Preparation for functional testing'''
        self.membership = getToolByName(self.portal, 'portal_membership', None)
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

        # Add users and add members to DiscussionManager group
        addMembers(self.portal, USERS)
        add2Group(self.portal, 'DiscussionManager', DM_USERS_IDS)
        self.createMemberarea('owner')

        ## Prepare mail sending - enter an e-mail adress, and allow all possible notifications
        setProperties(self.prefs, 'enable_moderation', 'enable_approve_notification',
                                  'enable_approve_user_notification','enable_reply_user_notification',
                                  'enable_published_notification', 'enable_rejected_user_notification')
        self.prefs._updateProperty('email_discussion_manager', 'discussion.manager@test.com')

        ## Add testing document to portal
        self.login('owner')
        self.portal.Members['owner'].invokeFactory('Document', id='my_doc', title="Test document")
        self.my_doc = self.portal.Members['owner']['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')

        ## Create talkback for document and Prepare REQUEST
        self.discussion.getDiscussionFor(self.my_doc)

        prepareMailSendTest()

    def checkToANDSubj(self, mails, to, subj):
        messages = [m for m in mails if REXP_TO.search(m) and REXP_TO.search(m).group(1)==to]
        self.assert_(len(messages) > 0, "No message sent to '%s' recipient" % to)
        self.assert_([1 for m in messages if REXP_SUBJ.search(m) and REXP_SUBJ.search(m).group(1)==subj],\
                     "There is no message for '%s' recipient with '%s' subject" % (to,subj))

    def test_Reply(self):
        cleanOutputDir()
        self.prepareRequest4Reply('replier1')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')

        mails = getMails()
        self.assertEqual(len(mails), 1)
        self.checkToANDSubj(mails, to="discussion.manager@test.com", subj="New comment awaits moderation")


    def test_PublishReply(self):
        self.prepareRequest4Reply('replier1')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.login('dm_admin')
        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        cleanOutputDir()

        reply.discussion_publish_comment()
        mails = getMails()
        self.assertEqual(len(mails), 2)
        self.checkToANDSubj(mails, to="owner@test.com", subj="New comment added")
        self.checkToANDSubj(mails, to="replier1@test.com", subj="Your comment on 'Test document' is now published")

    def test_Publish2ndReply(self):
        self.prepareRequest4Reply('replier1')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.login('dm_admin')
        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        reply.discussion_publish_comment()
        self.prepareRequest4Reply('replier2')
        reply.discussion_reply('A Reply for reply for my_doc' ,'text of reply on reply for my_doc')
        self.login('dm_admin')
        reply2 = self.discussion.getDiscussionFor(reply).getReplies()[0]
        cleanOutputDir()

        reply2.discussion_publish_comment()
        mails = getMails()
        self.assertEqual(len(mails), 3)
        self.checkToANDSubj(mails, to="owner@test.com", subj="New comment added")
        self.checkToANDSubj(mails, to="replier1@test.com", subj="Someone replied to your comment on 'Test document'")
        self.checkToANDSubj(mails, to="replier2@test.com", subj="Your comment on 'Test document' is now published")

    def test_DeleteReply(self):
        self.prepareRequest4Reply('replier1')
        self.my_doc.discussion_reply('A Reply for my_doc' ,'text of reply for my_doc')
        self.login('dm_admin')
        reply = self.discussion.getDiscussionFor(self.my_doc).getReplies()[0]
        cleanOutputDir()

        reply.deleteDiscussion()
        mails = getMails()
        self.assertEqual(len(mails), 1)
        self.checkToANDSubj(mails, to="replier1@test.com", subj="Your comment on 'Test document' was not approved.")


TESTS = [TestNotificationRecipients]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    for t in TESTS:
        suite.addTest(makeSuite(t))
    return suite

if __name__ == '__main__':
    framework()

