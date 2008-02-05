from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.tests import ArchetypesTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Products.PloneSMSCommunicator.pyXIAM import SMSsubmitRequest, getAllTextFromTag
from xml.dom.minidom import *
from StringIO import StringIO
import SimpleXiamServer
import BaseHTTPServer
import thread

ZopeTestCase.installProduct('PloneSMSCommunicator')

tests=[]

class SmSHandler(SimpleXiamServer.SimpleXiamHandler):

    server_url = None
    def testCommunicator(self):
        cl = int(self.headers['content-length'])
        doc = parseString(self.rfile.read(cl))
        self.assertEqual(getAllTextFromTag(doc, 'from')[0], '+380979312198')
        self.assertEqual(getAllTextFromTag(doc, 'to')[0], '+380979987348')
        self.assertEqual(getAllTextFromTag(doc, 'content')[0], 'hello how are you?')

    def do_POST(self):
        SimpleXiamServer.SimpleXiamHandler.do_POST(self)
        self.testCommunicator()


class TestPloneSMSCommunicator(ArchetypesTestCase.ArcheSiteTestCase, ZopeTestCase.Functional):

    httpd = BaseHTTPServer.HTTPServer(("", 10010), SmSHandler)

    def createManager(self, portal):

        acl_users = portal.acl_users
        return acl_users._doAddUser('PortalManager', '', ['Manager'], (), (), )

    def startServer(self):

        print 'serving at port', 10010
        self.httpd.serve_forever()

    def installProducts(self, portal):
        #create manager user
        self.createManager(portal)
        user = portal.acl_users.getUserById('PortalManager')

        #login as manager
        newSecurityManager(None, user)

        #install products
        qi = getToolByName(portal, 'portal_quickinstaller')
        qi.installProduct('PloneSMSCommunicator')

        #log out
        noSecurityManager()

    def afterSetUp(self):

        portal = self.portal
        self.installProducts(portal)

    def test_sendRequest(self):
        portal = self.portal
        #start new thread
        th = thread.start_new_thread(self.startServer, ())

        communicator = portal.portal_smsCommunicator
        communicator.setLogFlag(False)
        communicator.setServer('http://localhost:10010/')
        communicator.send_Request(originator = '+380979312198', destination = ['+380979987348'], body = 'hello how are you?')
        #destroy thread
        del th

    def test_Response(self):
        portal = self.portal
        communicator = portal.portal_smsCommunicator
        communicator.setLogFlag(False)
        response = """<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE xiamSMS SYSTEM "xiamSMSMessage.dtd">
                    <xiamSMS status="OK" statusText="XML contained 1 xir messages">
                     <submitResponse id="betye54">
                        <result status="OK" statusText="">+380979987348</result>
                     </submitResponse>
                    </xiamSMS>"""
        out = StringIO()
        out.write(response)
        communicator = portal.portal_smsCommunicator
        data = self.publish(portal.id+'/portal_smsCommunicator/Response', 'mgr:mgrpw', env=None, extra=None, request_method='POST', stdin = out)
        response = data.getBody()
        self.assertEqual(response, """<?xml version="1.0" ?>\n<!DOCTYPE  xiamSMS SYSTEM "xiamSMSMessage.dtd" >\n<xiamSMS status="OK"><submitRsponse id="betye54">XML contained your response messages</submitRsponse></xiamSMS>""")


tests.append(TestPloneSMSCommunicator)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneSMSCommunicator))
    return suite

if __name__ == '__main__':
    framework()