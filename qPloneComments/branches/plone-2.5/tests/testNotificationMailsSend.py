#
# Tests sending of notification mails
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from AccessControl.SecurityManagement import newSecurityManager
from helperNotify import *

PRODUCT = 'qPloneComments'
PROPERTY_SHEET = "qPloneComments"

PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite()


class TestNotificationMailsSend(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT)
        self.basic_auth = 'membr:secret'

        '''Preparation for functional testing'''
        self.discussion = self.portal.portal_discussion

        # Allow discussion for Document
        self.portal.portal_types.getTypeInfo('Document')._updateProperty('allow_discussion', 1)

        # Add testing document to portal
        self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')
        self.absolute_url = self.my_doc.absolute_url_path()

        prepareMailSendTest()
        self.logout()

    def testMemberAddComment(self):
        # Add new Member
        self.portal.portal_membership.addMember('membr', 'secret' , ['Member'], [])
        self.login(name='membr')
        user = self.portal.portal_membership.getAuthenticatedMember()
        user.setMemberProperties({'email':'comentar@test.com'})
        email = user.getProperty(id = 'email')

        # Create talkback for document and add comment
        talkback = self.discussion.getDiscussionFor(self.my_doc)
        talkback.createReply( title='test', text='blah' )

        # Publish comment after moderation
        path = '%s/prefs_recent_comments_form?form.submitted=1'%self.absolute_url
        extra = {'ids' : ['test']}
        self.publish(path, self.basic_auth, extra=extra)
        result = getFileContent(output_file_path('mail.res'))
        verifyMail(result, 'submit')


    def testMemberReplyComment(self):
        # Add new Member
        self.portal.portal_membership.addMember('membr', 'secret' , ['Member'], [])
        self.login(name='membr')
        user = self.portal.portal_membership.getAuthenticatedMember()
        user.setMemberProperties({'email':'comentar@test.com'})
        email = user.getProperty(id = 'email')

        # Create talkback for document add comment and reply for comment
        talkback = self.discussion.getDiscussionFor(self.my_doc)
        reply_id = talkback.createReply( title='test1', text='blah' )
        self.loginAsPortalOwner()
        reply1 = talkback.getReplies()[0]
        talkback1 = self.discussion.getDiscussionFor(reply1)
        talkback1.createReply( title='test2', text='blah2')

        # Publish comment after moderation
        path = '%s/prefs_recent_comments_form?form.submitted=1'%self.absolute_url
        extra = {'ids' : ['test2']}
        self.publish(path, self.basic_auth, extra=extra)
        result = getFileContent(output_file_path('mail.res'))
        verifyMail(result, 'reply')

    def testAnonymAddCommentWithEmail(self):
        self.logout()

    def testAnonymReplyCommentWithEmail(self):
        self.logout()

    def testAnonymAddCommentWithoutEmail(self):
        self.logout()

    def testAnonymReplyCommentWithoutEmail(self):
        self.logout()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNotificationMailsSend))
    return suite

if __name__ == '__main__':
    framework()
