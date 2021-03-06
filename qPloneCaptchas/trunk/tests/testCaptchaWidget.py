#
# Tests for qPloneCaptchas
#

import os, sys, re
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.qPloneCaptchas.utils import getWord, decrypt, parseKey
from Products.qPloneCaptchas.config import *

PloneTestCase.installProduct('PlacelessTranslationService')
PloneTestCase.installProduct('qPloneCaptchas')
PloneTestCase.setupPloneSite()

class TestCaptchaWidget(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct('qPloneCaptchas')
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
        path = '%s/discussion_reply_form'%self.absolute_url
        resp1 = self.publish(path, self.basic_auth, request_method='GET').getBody()
        patt = re.compile('\s+src="%s(/getCaptchaImage/[0-9a-fA-F]+)"'%self.portal.absolute_url())
        match_obj = patt.search(resp1)
        img_url = match_obj.group(1)
        content_type = self.publish('/plone'+img_url, self.basic_auth).getHeader('content-type')
        self.assert_(content_type.startswith('image'))

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
        patt = re.compile("Please re\-enter validation code")
        match_obj = patt.match(response)
        self.assert_(not match_obj)

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

class TestInstallation(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getToolByName(self.portal, 'portal_quickinstaller', None)
        self.cp = getToolByName(self.portal, 'portal_controlpanel', None)
        self.st = getToolByName(self.portal, 'portal_skins', None)
        self.qi.installProduct(PRODUCT_NAME)

    def getLayers(self):
        Layers = []
        Layers += LAYERS
        Layers.append(LAYER_STATIC_CAPTCHAS)
        DiscussionLayer = LAYER_DISCUSSION

        mtool = getToolByName(self, 'portal_migration')
        plone_version = mtool.getFileSystemVersion()
        if plone_version.startswith('2.1'):
            plone_version = '2.1.2'
        elif plone_version.startswith('2.0'):
            plone_version = '2.0.5'
        elif plone_version.startswith('2.5'):
            plone_version = '2.5'
        elif plone_version.startswith('3.0'):
            plone_version = '3.0'
        elif plone_version.startswith('3.1'):
            plone_version = '3.1'
        else:
            raise Exception("Error - Unsupported version. Suported versions: Plone 2.0.5-3")

        if self.qi.isProductInstalled('PloneFormMailer'):
            formmailer_layer = LAYER_FORMMAILER+'/'+ plone_version
            Layers.append(formmailer_layer)

        discussion_layer = '/'.join([DiscussionLayer, plone_version])
        Layers.append(discussion_layer)

        join_form_layer = '/'.join([LAYER_JOIN_FORM, plone_version])
        Layers.append(join_form_layer)

        sendto_form_layer = '/'.join([LAYER_SENDTO_FORM, plone_version])
        Layers.append(sendto_form_layer)

	return Layers

    def test_configlet_install(self):
        self.assert_(CONFIGLET_ID in [a.getId() for a in self.cp.listActions()], 'Configlet not found')

    def test_skins_install(self):
        skinstool = self.st
	Layers = self.getLayers()
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(str.strip, path.split(','))
	    for layer in Layers:
		self.assert_(layer.split('/')[0] in skinstool.objectIds(), '%s directory view not found in portal_skins after installation' % layer)
                self.assert_(layer in path, '%s layer not found in %s' % (PRODUCT_NAME, skin))

    def test_skins_uninstall(self):
        self.qi.uninstallProducts([PRODUCT_NAME])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT_NAME), True,'%s is already installed' % PRODUCT_NAME)
        skinstool = self.st
        Layers = self.getLayers()
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(str.strip, path.split(','))
	    for layer in Layers:
		self.assert_(not layer.split('/')[0] in skinstool.objectIds(), '%s directory view found in portal_skins after uninstallation' % layer)
                self.assert_(not layer in path, '%s layer found in %s after uninstallation' % (layer, skin))

    def test_configlet_uninstall(self):
        self.qi.uninstallProducts([PRODUCT_NAME])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT_NAME), True,'%s is already installed' % PRODUCT_NAME)
        self.assert_(not CONFIGLET_ID in [a.getId() for a in self.cp.listActions()], 'Configlet found after uninstallation')

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
