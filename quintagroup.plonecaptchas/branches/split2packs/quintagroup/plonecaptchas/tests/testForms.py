from base import *

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
            request_method='GET').getBody()
        open('/tmp/pc.image.html','w').write(response)
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
            extra=self.form_extra, request_method='GET').getBody()
        self.assertFalse(NOT_VALID.search(response))

    def testSubmitWrongCaptcha(self):
        self.form_extra['key'] = 'wrong word'
        response = self.publish(self.save_url, self.basic_auth,
            extra=self.form_extra, request_method='GET').getBody()
        self.assertTrue(NOT_VALID.search(response))

    def testSubmitRightCaptchaTwice(self):
        key = getWord(int(parseKey(decrypt(self.captcha_key, self.hashkey))['key'])-1)
        self.form_extra['key'] = key

        self.publish(self.save_url, self.basic_auth,
            extra=self.form_extra, request_method='GET')

        response = self.publish(self.save_url, self.basic_auth,
            extra=self.form_extra, request_method='GET').getBody()
        self.assertTrue(NOT_VALID.search(response))


class TestDiscussionForm(TestFormMixing):

    def afterSetUp(self):
        TestFormMixing.afterSetUp(self)
        self.portal.invokeFactory('Document', 'index_html')
        self.portal['index_html'].allowDiscussion(True)
        
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


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDiscussionForm))
    return suite
