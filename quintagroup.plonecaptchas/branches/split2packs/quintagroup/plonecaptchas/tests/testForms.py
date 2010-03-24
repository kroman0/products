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
        self.save_url = self.getSaveURL()


    def getSaveURL(self):
        raise NotImplementedError(
            "getSaveURL not implemented")

    def getExtras_submitRightCaptcha(self, hashkey, key):
        raise NotImplementedError(
            "getExtras_submitRightCaptcha not implemented")

    def getExtras_submitWrongCaptcha(self, hashkey):
        raise NotImplementedError(
            "getExtras_submitWrongCaptcha not implemented")


    def testImage(self):
        response = self.publish(self.save_url, self.basic_auth,
            request_method='GET').getBody()
        patt = re.compile(IMAGE_PATT  % self.portal.absolute_url())
        match_obj = patt.search(response)
        img_url = match_obj.group(1)

        content_type = self.publish('/plone' + img_url,
            self.basic_auth).getHeader('content-type')
        self.assertTrue(content_type.startswith('image'),
            "Wrong captcha image content type")

    def testSubmitRightCaptcha(self):
        hashkey = self.portal.getCaptcha()
        key = getWord(int(parseKey(decrypt(self.captcha_key, hashkey))['key'])-1)
        extra = self.getExtras_submitRightCaptcha(hashkey, key)
        
        response = self.publish(self.save_url, self.basic_auth,
            extra=extra, request_method='GET').getBody()
        self.assertFalse(NOT_VALID.search(response))

    def testSubmitWrongCaptcha(self):
        hashkey = self.portal.getCaptcha()
        extra = self.getExtras_submitWrongCaptcha(hashkey)

        response = self.publish(self.save_url, self.basic_auth,
            extra=extra, request_method='GET').getBody()
        self.assertTrue(NOT_VALID.search(response))

    def testSubmitRightCaptchaTwice(self):
        hashkey = self.portal.getCaptcha()
        key = getWord(int(parseKey(decrypt(self.captcha_key, hashkey))['key'])-1)
        extra = self.getExtras_submitRightCaptcha(hashkey, key)

        self.publish(self.save_url, self.basic_auth,
            extra=extra, request_method='GET')

        response = self.publish(self.save_url, self.basic_auth,
            extra=extra, request_method='GET').getBody()
        self.assertTrue(NOT_VALID.search(response))


class TestDiscussionForm(TestFormMixing):

    def afterSetUp(self):
        TestFormMixing.afterSetUp(self)
        # prepare discussion object
        self.portal.invokeFactory('Document', 'index_html')
        self.portal['index_html'].allowDiscussion(True)


    def getSaveURL(self):
        return self.portal['index_html'].absolute_url(1) + \
            '/discussion_reply_form?form.submitted=1' + \
            '&form.button.form_submit=Save'

    def getExtras_submitRightCaptcha(self, hashkey, key):
        return {'form.submitted' : '1',
                'Creator': portal_owner,
                'key' : key,
                'hashkey': hashkey,
                'subject': 'testing',
                'body_text': 'Text in Comment',
                'discussion_reply:method': 'Save'}

    def getExtras_submitWrongCaptcha(self, hashkey):
        return {'form.submitted' : '1',
                'Creator': portal_owner,
                'key' : 'wrong word',
                'hashkey': hashkey,
                'subject': 'testing',
                'body_text': 'Text in Comment',
                'discussion_reply:method': 'Save'}


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDiscussionForm))
    return suite
