from Products.CMFCore.CMFCorePermissions import AddPortalContent, ManagePortal
import os

GLOBALS=globals()
PROJECTNAME="PloneSMSCommunicator"
SKINS_DIR = 'skins'
ADD_CONTENT_PERMISSION=AddPortalContent
COMMUNICATORID="portal_smsCommunicator"
PROVIDER='172'
SERVER_URL='http://193.95.160.218:8080/smsxml/collector'
CLIENT_HOME = os.environ.get("CLIENT_HOME")
XIAM_LOG = CLIENT_HOME + '/xiam.log'
SMS_LOG = CLIENT_HOME + '/sms/'
SMSCOMMUNICATOR_MP = ManagePortal
ORIGINATOR = "51101"
IP_ADDRESS = '66.135.39.161'
SERVER_NAME = 'sms.quintagroup.com'
RESPONCE_FUNC = '/sms/portal_smsCommunicator/processResponce'