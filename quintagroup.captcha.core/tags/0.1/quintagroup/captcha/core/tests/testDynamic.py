import string
from base import *

from DateTime import DateTime
from Products.CMFFormController.ControllerState import ControllerState

from testStatic import TestStaticValidator

class DynamicMixin:
    def switchToDynamic(self):
        skins = self.portal.portal_skins
        for skin in skins.getSkinSelections():
            path = skins.getSkinPath(skin)
            path = map( string.strip, string.split( path,',' ))
            try:
                i = path.index(LAYER_STATIC_CAPTCHAS)
                path.remove(LAYER_STATIC_CAPTCHAS)
                path.insert(i, LAYER_DYNAMIC_CAPTCHAS)
            except ValueError:
                pass
            path = string.join( path, ', ' )
            skins.addSkinSelection( skin, path )
            self._refreshSkinData()

class TestDynamic(DynamicMixin, ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        self.skins = self.portal.portal_skins
        self.switchToDynamic()

        self.captcha_key = self.portal.captcha_key
        self.hashkey = self.portal.getCaptcha()

    def test_GetCaptcha_Date(self):
        # *date* must present after parsing decrypted key
        decrypted_key = decrypt(self.captcha_key, self.hashkey)
        parsed_key = parseKey(decrypted_key)
        self.assertTrue('date' in parsed_key.keys())

    def test_GetCaptcha_Key(self):
        decrypted_key = decrypt(self.captcha_key, self.hashkey)
        parsed_key = parseKey(decrypted_key)
        # *key* must present after parsing decrypted key
        self.assertTrue('key' in parsed_key.keys())
        # index start from 0 and lower or equals to captchas count
        index = int(parsed_key['key'])
        self.assertTrue(index >= 0 and index <= len(utils.basic_english.words.split()))
        # encrypted key must be equals to word from the dictionary,
        # under index position and must be not empty string
        self.assertFalse(getWord(index) == "")

    def test_GetImage(self):
        # getCaptchaImage function must return image coded in hashkey same to
        # image get by 'key' after parsing decrypted key 
        decrypted_key = decrypt(self.captcha_key, self.hashkey)
        parsed_key = parseKey(decrypted_key)

        img_html = self.publish(
            self.portal.absolute_url(1)+"/getCaptchaImage/%s" % self.hashkey)

        img_ctype = img_html.getHeader('content-type')
        self.assertTrue(img_ctype == 'image/jpeg', "Wrong content type for " \
            "generated image: %s, must be 'image/jpeg'" % img_ctype)
        self.assertTrue(img_html.status == 200, "Wrong response status: " \
            "'%s', must be '200'" % img_html.status)
        

class TestDynamicValidator(DynamicMixin, TestStaticValidator):

    def afterSetUp(self):
        TestStaticValidator.afterSetUp(self)
        self.switchToDynamic()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDynamic))
    suite.addTest(unittest.makeSuite(TestDynamicValidator))
    return suite
