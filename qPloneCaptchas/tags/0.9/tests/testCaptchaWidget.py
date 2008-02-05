#
# Skeleton PloneTestCase
#

import os, sys, re
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from AccessControl.SecurityManagement import newSecurityManager
from Products.qPloneCaptchas.utils import getWord, decrypt, parseKey

PloneTestCase.installProduct('qPloneCaptchas')
PloneTestCase.setupPloneSite()

class TestCaptchaWidget(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct('qPloneCaptchas')
        self.portal.invokeFactory('Document', 'index_html')
        self.portal['index_html'].allow_discussion = True
        self.absolute_url = self.portal['index_html'].absolute_url_path()

        self.basic_auth = 'portal_manager:secret'
        uf = self.app.acl_users
        uf.userFolderAddUser('portal_manager', 'secret', ['Manager'], [])
        user = uf.getUserById('portal_manager')
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)
        self.captcha_key = self.portal.captcha_key
    
    def testSubmitRightCaptcha(self):
        hashkey = self.portal.getCaptcha()
        key = getWord(int(parseKey(decrypt(self.captcha_key, hashkey))['key']))
        parameters = 'form.submitted=1&Creator=test_user&key=%s'%key
        path = '%s/discussion_reply_form?%s'%(self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'subject': 'testing',
                 'body_text': 'Text in Comment',
                 'discussion_reply:method': 'Save'}

        response = self.publish(path, self.basic_auth, extra=extra, request_method='GET').getBody()
        patt = re.compile(".*?Comment\+added")
        match_obj = patt.match(response)
        self.assert_(match_obj)


    
    def testSubmitWrongCaptcha(self):
        hashkey = self.portal.getCaptcha()
        parameters = 'form.submitted=1&Creator=test_user&key=fdfgh'
        path = '%s/discussion_reply_form?%s'%(self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'subject': 'testing',
                 'body_text': 'Text in Comment',
                 'discussion_reply:method': 'Save'}

        response = self.publish(path, self.basic_auth, extra=extra, request_method='GET').getBody()
        patt = re.compile("Please re\-enter validation code")
        match_obj = patt.search(response)
        self.assert_(match_obj)
    
    def testSubmitRightCaptchaTwice(self):
        hashkey = self.portal.getCaptcha()
        key = getWord(int(parseKey(decrypt(self.captcha_key, hashkey))['key']))
        parameters = 'form.submitted=1&Creator=test_user&key=%s'%key
        path = '%s/discussion_reply_form?%s'%(self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'subject': 'testing',
                 'body_text': 'Text in Comment',
                 'discussion_reply:method': 'Save'}

        self.publish(path, self.basic_auth, extra=extra, request_method='GET')
        response = self.publish(path, self.basic_auth, extra=extra, request_method='GET').getBody()
        patt = re.compile(".*?Comment\+added")
        match_obj = patt.match(response)
        self.assert_(not match_obj)
    
    def testSubmitExpiredCaptcha(self):
        pass
        """
        hashkey = self.portal.getCaptcha()
        key = getWord(int(parseKey(decrypt(self.captcha_key,hashkey))['key']))
        parameters = 'form.submitted=1&Creator=test_user&key=%s'%key
        path = '%s/discussion_reply_form?%s'%(self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'subject': 'testing',
                 'body_text': 'Text in Comment',
                 'discussion_reply:method': 'Save'}
                
        from DateTime import DateTime
        last = repr(DateTime().timeTime())
        import time
        DateTime._t = time.time() + 3601.0
        raise repr(DateTime().timeTime())+' '+last
                
        response = self.publish(path, self.basic_auth, extra=extra, request_method='GET').getBody()
        DateTime._t = time.time()
        patt = re.compile(".*?Comment\+added")
        match_obj = patt.match(response)
        self.assert_(match_obj)
        """

class TestInstallation(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct('qPloneCaptchas')
    
    def testCaptchaKey(self):
        ck = getattr(self.portal, 'captcha_key')
        self.assert_(ck)
        self.assertEqual(len(ck), 8)
    
    def testCaptchaTool(self):
        self.assert_('portal_captchas' in self.portal.objectIds())
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCaptchaWidget))
    suite.addTest(makeSuite(TestInstallation))
    return suite

if __name__ == '__main__':
    framework()

