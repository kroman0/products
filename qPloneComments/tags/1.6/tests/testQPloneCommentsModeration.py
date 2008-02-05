#
# Test moderation behavior
#

import os, sys, string
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
import re

PRODUCT = 'qPloneComments'
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


class TestModeration(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        self.qi = getToolByName(self.portal, 'portal_quickinstaller', None)
        self.qi.installProduct(PRODUCT)
        # VERY IMPORTANT to guarantee product skin's content visibility
        self._refreshSkinData()

        '''Preparation for functional testing'''
        # By default on installation terning on moderation and anonymus commenting
        # But if that changes. Following 4 lines must be uncommenting
        #self.request = self.app.REQUEST
        #self.request.form['Enable_Anonymous_Commenting'] = 'True'
        #self.request.form['Enable_Moderation'] = 'True'
        #self.portal.prefs_comments_setup()

        # Add all users
        self.membership = getToolByName(self.portal, 'portal_membership', None)
        for user_id in USERS.keys():
            self.membership.addMember(user_id, USERS[user_id]['passw'] , USERS[user_id]['roles'], [])
        
        # Add users to Discussion Manager group
        portal_groups = getToolByName(self.portal, 'portal_groups')
        #portal_groups.addGroup('DiscussionManager', roles=['DiscussionManager'])
        dm_group = portal_groups.getGroupById(id='DiscussionManager')
        dm_users = [dm_group.addMember(u) for u in DM_USERS_IDS]

        # Allow discussion for Document
        portal_types = getToolByName(self.portal, 'portal_types', None)
        doc_fti = portal_types.getTypeInfo('Document')
        doc_fti._updateProperty('allow_discussion', 1)

        # Add testing documents to portal. Add one document for avery user.
        # For testing behaviors, where made some changes to document state it's more usefull.
        self.discussion = getToolByName(self.portal, 'portal_discussion', None)
        all_users_id = DM_USERS_IDS + COMMON_USERS_IDS
        for user_id in all_users_id:
            doc_id = 'doc_%s' % user_id
            self.portal.invokeFactory('Document', id=doc_id)
            doc_obj = getattr(self.portal, doc_id)
            doc_obj.edit(text_format='plain', text='hello world from %s' % doc_id)
            # Create talkback for document and Add comment to doc_obj
            self.discussion.getDiscussionFor(doc_obj)
            doc_obj.discussion_reply('A Reply for %s' % doc_id,'text of reply for %s' % doc_id)


    ## TEST VIEWING

    def testViewRepliesNotPublishedDMUsers(self):
        # All members of DiscussionManager group MUST VIEW comments
        doc = getattr(self.portal, 'doc_%s' % DM_USERS_IDS[0])
        for u in DM_USERS_IDS:
            self.logout()
            self.login(u)
            replies = self.discussion.getDiscussionFor(doc).getReplies()
            self.assert_(replies, "Viewing discussion item forbiden for %s - member of DiscussionManager group" % u)


    def testViewRepliesNotPublishedNotDMUsers(self):
        # All common users SHOULD NOT VIEW NOT PUBLISHED comments
        doc = getattr(self.portal, 'doc_%s' % DM_USERS_IDS[0])
        for u in COMMON_USERS_IDS:
            self.logout()
            if not u=='anonym':
                self.login(u)
            replies = self.discussion.getDiscussionFor(doc).getReplies()
            self.assert_(not replies, "Viewing of NOT published discussion item allow %s - user without DiscussionManager role" % u)


    def testViewRepliesPublishedAllUsers(self):
        # All users MUST VIEW PUBLISHED comments
        # Get any document and publish it's comment
        doc = getattr(self.portal, 'doc_%s' % 'dm_admin')
        self.login('dm_admin')
        di = self.discussion.getDiscussionFor(doc).getReplies()[0]
        di.discussion_publish_comment()
        
        all_users_id = USERS.keys() + ['anonym']
        for u in all_users_id:
            self.logout()
            if not u=='anonym':
                self.login(u)
            replies = self.discussion.getDiscussionFor(doc).getReplies()
            self.assert_(replies, "Viewing PUBLISHED discussion item forbiden for %s user" % u)


    ## TEST PUBLISHING    

    def testViewPublishButtonNonDMUsers(self):
        # Publish button MUST BE ABSENT in document view form 
        # Pattern for publish button presence checking
        pattern = re.compile('.*<input\\s*class="standalone"\\s*type="submit"\\s*value="Publish This Discussion"\\s*/>',\
                             re.S|re.M)
        for u in COMMON_USERS_IDS:
            self.logout()
            auth = u
            if not u=='anonym':
                self.login(u)
                auth = '%s:%s' % (u,USERS[u]['passw'])
            doc_id = "doc_%s" % u
            html = str(self.publish(self.portal.id+'/%s' % doc_id, auth))
            m = pattern.match(html)
            self.assert_(not m, "Publish button present for %s - user without DiscussionManager role" % u)
    

    def testViewPublishButtonDMUsers(self):
        # Publish button MUST PRESENT in document view form 
        # Pattern for publish button presence checking
        pattern = re.compile('.*<input\\s*class="standalone"\\s*type="submit"\\s*value="Publish This Discussion"\\s*/>',\
                             re.S|re.M)
        for u in DM_USERS_IDS:
            self.logout()
            self.login(u)
            auth = '%s:%s' % (u,USERS[u]['passw'])
            doc_id = "doc_%s" % u
            html = str(self.publish(self.portal.id+'/%s' % doc_id, auth))
            m = pattern.match(html)
            self.assert_(m, "Publish button NOT PRESENT for %s - member of DiscussionManager group" % u)


    def testPublishing(self):
        # Check whether perform real publishing
        for u in DM_USERS_IDS:
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            getReplies = self.discussion.getDiscussionFor(doc_obj).getReplies
            # Check whether anonymous get no reply
            self.logout()
            self.assert_(not getReplies(), "View not published reply ALLOW for Anonymous")
            # Login with actual (tested) user with DiscussionManager role and publish discussion
            self.login(u)
            self.assert_(getReplies(), "%s - member of DiscussionManager group NOT VIEW not published reply" % u)
            getReplies()[0].discussion_publish_comment()
            # Check whether Anonym view published reply
            self.logout()
            self.assert_(getReplies(), "%s - member of DiscussionManager group NOT PUBLISH reply" % u)

    
    ## TEST DELETING

    def testViewDeleteButtonNonDMUsers(self):
        # Check Delete reply button presense ONLY for PUBLISHED reply.
        # Because of NOT PUBLUISHED replies is not visible at all for common users.
        # Delete reply button in document view form MUST BE ABSENT for all EXCEPT manager.
        # Publish replies
        self.logout()
        self.login('dm_admin')
        for u in COMMON_USERS_IDS:
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
            reply.discussion_publish_comment()
        # Prepare pattern for delete reply button presence checking
        pattern = re.compile('.*<input\\s*class="destructive"\\s*type="submit"\\s*value="Remove This Discussion"\\s*/>',\
                             re.S|re.M)
        for u in COMMON_USERS_IDS:
            self.logout()
            auth = u
            if not u=='anonym':
                self.login(u)
                auth = '%s:%s' % (u,USERS[u]['passw'])
            doc_id = "doc_%s" % u
            html = str(self.publish(self.portal.id+'/%s' % doc_id, auth))
            m = pattern.match(html)
            if not u=='anonym' and 'Manager' in USERS[u]['roles']:
                self.assert_(m, "%s - user with Manager role NOT VIEW Delete reply button for published reply on document view form" % u)
            else:
                self.assert_(not m, "%s - user without Manager role CAN VIEW Delete reply button for published reply on document view form" % u)
    

    def testViewDeleteButtonDMUsers(self):
        # Delete reply button in document view form MUST BE ABSENT for all EXCEPT manager.
        # Prepare pattern for delete reply button presence checking
        pattern = re.compile('.*<input\\s*class="destructive"\\s*type="submit"\\s*value="Remove This Discussion"\\s*/>',\
                             re.S|re.M)
        for u in DM_USERS_IDS:
            self.logout()
            self.login(u)
            auth = '%s:%s' % (u,USERS[u]['passw'])
            doc_id = "doc_%s" % u
            html = str(self.publish(self.portal.id+'/%s' % doc_id, auth))
            m = pattern.match(html)
            if 'Manager' in USERS[u]['roles']:
                self.assert_(m, "%s - user with Manager role NOT VIEW Delete reply button on document view form" % u)
            else:
                self.assert_(not m, "%s - user without Manager role CAN VIEW Delete reply button on document view form" % u)


    def testDeleting(self):
        # Manager with DiscussionManager role CAN delete ANY REPLY.
        # Manager without DiscussionManager role [common manager] CAN delete ONLY PUBLISHED REPLY.
        # Get Managers
        managers = [u for u in USERS.keys() if 'Manager' in USERS[u]['roles']]
        dm_man = [u for u in managers if u.startswith('dm_')][0]
        common_man = [u for u in managers if not u.startswith('dm_')][0]
        # Publish document for common manager
        self.logout()
        self.login(dm_man)
        doc_obj = getattr(self.portal, "doc_%s" % common_man)
        reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
        reply.discussion_publish_comment()
        # Check for really deleting
        for u in managers:
            self.logout()
            self.login(u)
            auth = '%s:%s' % (u,USERS[u]['passw'])
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            getReplies = self.discussion.getDiscussionFor(doc_obj).getReplies
            self.assert_(getReplies(), "%s - user with Manager role not view discussion reply" % u)
            getReplies()[0].deleteDiscussion()
            self.assert_(not getReplies(), "%s - user with Manager role not really delete discussion" % u)


TESTS = [TestModeration]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestModeration))
    return suite

if __name__ == '__main__':
    framework()

