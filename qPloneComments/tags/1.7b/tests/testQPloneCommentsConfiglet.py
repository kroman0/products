#
# Test configuration form working
#

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal, ReplyToItem
import socket

PRODUCT = 'qPloneComments'
PROPERTY_SHEET = "qPloneComments"

USERS = {# Common Members
         'admin':{'passw': 'secret_admin', 'roles': ['Manager']},
         'owner':{'passw': 'secret_owner', 'roles': ['Owner']},
         'member':{'passw': 'secret_member', 'roles': ['Member']},
         'reviewer':{'passw': 'secret_reviewer', 'roles': ['Reviewer']},
         # Members for discussion manager group
         'dm_admin':{'passw': 'secret_dm_admin', 'roles': ['Manager']},
         'dm_owner':{'passw': 'secret_dm_owner', 'roles': ['Owner']},
         'dm_member':{'passw': 'secret_dm_member', 'roles': ['Member']},
         'dm_reviewer':{'passw': 'secret_dm_reviewer', 'roles': ['Reviewer']},
        }
COMMON_USERS_IDS = [u for u in USERS.keys() if not u.startswith('dm_')]
COMMON_USERS_IDS.append('anonym')
DM_USERS_IDS = [u for u in USERS.keys() if u.startswith('dm_')]

PloneTestCase.installProduct(PRODUCT)
PloneTestCase.setupPloneSite()

def addUsers(self):
    self.loginAsPortalOwner()
    # Add all users
    self.membership = getToolByName(self.portal, 'portal_membership', None)
    for user_id in USERS.keys():
        self.membership.addMember(user_id, USERS[user_id]['passw'] , USERS[user_id]['roles'], [])
    
    # Add users to Discussion Manager group
    portal_groups = getToolByName(self.portal, 'portal_groups')
    #portal_groups.addGroup('DiscussionManager', roles=['DiscussionManager'])
    dm_group = portal_groups.getGroupById(id='DiscussionManager')
    dm_users = [dm_group.addMember(u) for u in DM_USERS_IDS]
    

class TestConfiglet(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(PRODUCT)
        # VERY IMPORTANT to guarantee product skin's content visibility
        self._refreshSkinData()

        '''Preparation for functional testing'''
        # Allow discussion for Document
        portal_types = getToolByName(self.portal, 'portal_types', None)
        doc_fti = portal_types.getTypeInfo('Document')
        doc_fti._updateProperty('allow_discussion', 1)

        # Add testing document to portal
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')

        portal_properties = getToolByName(self.portal, 'portal_properties', None)
        self.prefs = portal_properties[PROPERTY_SHEET]
        self.request = self.app.REQUEST


    def testAnonymousCommenting(self):
        getPortalReplyPerm = self.portal.rolesOfPermission
        def getReplyRoles():
            return [r['name'] for r in getPortalReplyPerm(ReplyToItem) if r['selected']=='SELECTED']
        # Simulate switching ON Anonymous Commenting
        self.request.form['Enable_Anonymous_Commenting'] = 'True'
        self.portal.prefs_comments_setup()
        actual_reply_permission = getReplyRoles()
        self.assert_('Anonymous' in actual_reply_permission, \
                     "'Reply to Item' permission set for %s. 'Anonymous' role NOT added" %  actual_reply_permission)
        # Simulate switching OFF Anonymous Commenting
        if self.request.form.has_key('Enable_Anonymous_Commenting'):
           del self.request.form['Enable_Anonymous_Commenting']
        self.portal.prefs_comments_setup()
        actual_reply_permission = getReplyRoles()
        self.assert_(not 'Anonymous' in actual_reply_permission, \
                     "'Reply to Item' permission set for %s. 'Anonymous' role NOT erased" %  actual_reply_permission)


    def testSwitchONModeration(self):
        addUsers(self)
        self.discussion = self.portal.portal_discussion
        self.request.form['Enable_Anonymous_Commenting'] = 'True'
        self.request.form['Enable_Moderation'] = 'True'
        self.portal.prefs_comments_setup()
        # Create talkback for document and Add comment to my_doc
        self.discussion.getDiscussionFor(self.my_doc)
        self.my_doc.discussion_reply('Reply 1','text of reply')
        # Check moderating discussion
        # MUST ALLOW for: members of 'DiscussionMnagers' group
        # MUST REFUSE for: NOT members of 'DiscussionMnagers' group
        getReplies = self.discussion.getDiscussionFor(self.my_doc).getReplies
        for u in DM_USERS_IDS:
            self.logout()
            self.login(u)
            self.assert_(getReplies(), "None discussion item added or discussion forbiden for %s user" % u)
        for u in COMMON_USERS_IDS:
            self.logout()
            if not u=='anonym':
                self.login(u)
            self.assert_(not getReplies(), "Viewing discussion item allow for Anonymous user")

        
    def testSwitchOFFModeration(self):
        addUsers(self)
        self.discussion = self.portal.portal_discussion
        self.request.form['Enable_Anonymous_Commenting'] = 'True'
        self.portal.prefs_comments_setup()
        # Create talkback for document and Add comment to my_doc
        self.discussion.getDiscussionFor(self.my_doc)
        self.request.form['Creator'] = self.portal.portal_membership.getAuthenticatedMember().getUserName()
        self.request.form['subject'] = "Reply 1"
        self.request.form['body_text'] = "text of reply"
        self.my_doc.discussion_reply('Reply 1','text of reply')
        # Check moderating discussion
        # MUST ALLOW for: user with any role or Anonym
        all_users_ids = DM_USERS_IDS + COMMON_USERS_IDS
        for u in all_users_ids:
            self.logout()
            if not u=='anonym':
                self.login(u)
            replies = self.discussion.getDiscussionFor(self.my_doc).getReplies()
            self.assert_(replies, "No discussion item added or discussion forbidden for %s user" % u)


    def testNotification(self):
        # For prepare mail sending - enter an e-mail adress
        self.prefs._updateProperty('Email_Discussion_Manager', 'wrong_email_addr')
        # Create talkback for document and Prepare REQUEST
        self.portal.portal_discussion.getDiscussionFor(self.my_doc)
        self.request.form['Creator'] = self.portal.portal_membership.getAuthenticatedMember().getUserName()
        self.request.form['subject'] = "Reply 1"
        self.request.form['body_text'] = "text of reply"

        # Check Notification ON
        self.assert_(self.prefs.getProperty('Enable_Notification')==1,"Notification not terned ON")
        self.assertRaises(socket.error, self.my_doc.discussion_reply, 'Reply 1', 'text of reply')
        # Check Notification OFF
        self.prefs._updateProperty('Enable_Notification', 0)
        self.assert_(self.prefs.getProperty('Enable_Notification')==0,"Notification not terned Off")
        try:
            self.my_doc.discussion_reply('Reply 1','text of reply')
        except socket.error:
            self.fail("Terning notification Off NOT work")


TESTS = [TestConfiglet]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestConfiglet))
    return suite

if __name__ == '__main__':
    framework()

