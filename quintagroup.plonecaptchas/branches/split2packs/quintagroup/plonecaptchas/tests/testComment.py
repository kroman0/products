from base import *

class TestContactForm(FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        self.portal.invokeFactory('Document', 'index_html')
        self.portal['index_html'].allowDiscussion(True)
        self.absolute_url = self.portal['index_html'].absolute_url_path()

        self.basic_auth = 'portal_manager:secret'
        uf = self.app.acl_users
        uf.userFolderAddUser('portal_manager', 'secret', ['Manager'], [])
        user = uf.getUserById('portal_manager')
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)
        self.captcha_key = self.portal.captcha_key

    def testImage(self):
        path = '%s/discussion_reply_form' % self.absolute_url
        response = self.publish(path, self.basic_auth, request_method='GET').getBody()
        patt = re.compile('\s+src="%s(/getCaptchaImage/[0-9a-fA-F]+)"' % self.portal.absolute_url())
        match_obj = patt.search(response)
        img_url = match_obj.group(1)
        content_type = self.publish('/plone' + img_url, self.basic_auth).getHeader('content-type')
        self.assert_(content_type.startswith('image'))

    def testSubmitRightCaptcha(self):
        hashkey = self.portal.getCaptcha()
        key = getWord(int(parseKey(decrypt(self.captcha_key, hashkey))['key']))
        parameters = 'form.submitted=1&Creator=test_user&key=%s' % key
        path = '%s/discussion_reply_form?%s' % (self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'subject': 'testing',
                 'body_text': 'Text in Comment',
                 'discussion_reply:method': 'Save'}
        response = self.publish(path, self.basic_auth, extra=extra, request_method='GET').getBody()
        patt = re.compile("Please re\-enter validation code")
        match_obj = patt.match(response)
        self.assert_(not match_obj)

    def testSubmitWrongCaptcha(self):
        hashkey = self.portal.getCaptcha()
        parameters = 'form.submitted=1&Creator=test_user&key=fdfgh'
        path = '%s/discussion_reply_form?%s' % (self.absolute_url, parameters)
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


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestContactForm))
    return suite
