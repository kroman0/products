from base import *
from DateTime import DateTime

# USE PATCH FROM quintagroup.captcha.core
# patch to use test images and dictionary
testPatch()

class TestFormMixing(FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        # Add test_captcha layer from quintagroup.captcah.core
        addTestLayer(self)

        self.basic_auth = ':'.join((portal_owner,default_password))
        self.captcha_key = self.portal.captcha_key

        self.hashkey = self.portal.getCaptcha()
        self.req_method = self.getRequestMethod()
        self.save_url = self.getSaveURL()
        self.form_extra = self.getFormExtra()
        self.form_extra['hashkey'] = self.hashkey
        self.form_extra['key'] = ''

    def getSaveURL(self):
        raise NotImplementedError(
            "getSaveURL not implemented")

    def getFormExtra(self):
        raise NotImplementedError(
            "getFormExtra not implemented")
        
    def testImage(self):
        response = self.publish(self.save_url, self.basic_auth,
            request_method=self.req_method).getBody()
        patt = re.compile(IMAGE_PATT  % self.portal.absolute_url())
        match_obj = patt.search(response)
        img_url = match_obj.group(1)

        content_type = self.publish('/plone' + img_url,
            self.basic_auth).getHeader('content-type')
        self.assertTrue(content_type.startswith('image'),
            "Wrong captcha image content type")

    def testSubmitRightCaptcha(self):
        key = getWord(int(parseKey(decrypt(self.captcha_key, self.hashkey))['key'])-1)
        self.form_extra['key'] = key
        
        response = self.publish(self.save_url, self.basic_auth,
            extra=self.form_extra, request_method=self.req_method).getBody()
        self.assertFalse(NOT_VALID.search(response))

    def testSubmitWrongCaptcha(self):
        self.form_extra['key'] = 'wrong word'
        response = self.publish(self.save_url, self.basic_auth,
            extra=self.form_extra, request_method=self.req_method).getBody()
        self.assertTrue(NOT_VALID.search(response))

    def testSubmitRightCaptchaTwice(self):
        key = getWord(int(parseKey(decrypt(self.captcha_key, self.hashkey))['key'])-1)
        self.form_extra['key'] = key

        self.publish(self.save_url, self.basic_auth,
            extra=self.form_extra, request_method=self.req_method)

        response = self.publish(self.save_url, self.basic_auth,
            extra=self.form_extra, request_method=self.req_method).getBody()
        
        open('/tmp/pc.rct.html','w').write(response)
        self.assertTrue(NOT_VALID.search(response))


class TestDiscussionForm(TestFormMixing):

    def afterSetUp(self):
        TestFormMixing.afterSetUp(self)
        self.portal.invokeFactory('Document', 'index_html')
        self.portal['index_html'].allowDiscussion(True)
        
    def getRequestMethod(self):
        return "GET"

    def getSaveURL(self):
        return self.portal['index_html'].absolute_url(1) + \
            '/discussion_reply_form?form.submitted=1' + \
            '&form.button.form_submit=Save'

    def getFormExtra(self):
        return {'form.submitted' : '1',
                'Creator': portal_owner,
                'subject': 'testing',
                'body_text': 'Text in Comment',
                'discussion_reply:method': 'Save'}


class TestJoinForm(TestFormMixing):

    def _getauth(self):
        # Fix authenticator for the form
        authenticator = self.portal.restrictedTraverse("@@authenticator")
        html = authenticator.authenticator()
        handle = re.search('value="(.*)"', html).groups()[0]
        return handle

    def getRequestMethod(self):
        return "POST"

    def getSaveURL(self):
        return self.portal.absolute_url(1) + \
            '/join_form?form.button.Register=Register' + \
            '&form.submitted=1'

    def getFormExtra(self):
        return {"last_visit:date" : str(DateTime()),
                "prev_visit:date" : str(DateTime()),
                "came_from_prefs" : "",
                "fullname" : "Tester",
                "username" : "tester",
                "email" : "tester@test.com",
                '_authenticator' : self._getauth()}


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDiscussionForm))
    suite.addTest(unittest.makeSuite(TestJoinForm))
    return suite
