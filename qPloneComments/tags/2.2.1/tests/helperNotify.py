#########################################################
##      Helper methods for testing Mail sending        ##
#########################################################

import sys
import os, os.path
from Products.MailHost.MailHost import MailBase
ver = "2.0.5"
try:
    from Products.SecureMailHost.SecureMailHost import SecureMailBase
    ver = "2.1"
except ImportError:
    pass

PREFIX = os.path.abspath(os.path.dirname(__file__))

ALL_PROPS = ['enable_approve_user_notification', 'enable_reply_user_notification',
             'enable_rejected_user_notification','enable_moderation',
             'require_email', 'enable_anonymous_commenting',
             'enable_published_notification', 'enable_approve_notification']

def sample_file_path(file):
    return os.path.join(PREFIX, 'sample', file)

def output_file_path(file):
    return os.path.join(PREFIX, 'output', file)

def getFileContent(f_path):
    result_f = open(f_path,"r")
    result = result_f.read()
    result_f.close()
    return result

def writeToFile(f_path, text):
    result_f = open(f_path,'w')
    result_f.write(text+'\n')
    result_f.close()

def clearFile(f_path):
    result_f = open(f_path,"w")
    result_f.write('')
    result_f.close()

def _send_MH( self, mfrom, mto, messageText ):
    files = [f for f in os.listdir('./output') if f.startswith('mail')]
    fn = files[-1]+ '1'
    writeToFile(output_file_path(fn), messageText)

def _send_SMH(self, mfrom, mto, messageText, debug=False):
    files = [f for f in os.listdir('./output') if f.startswith('mail')]
    fn = files[-1]+ '1'
    writeToFile(output_file_path(fn), messageText)

def send_SMH(self, message, mto=None, mfrom=None, subject=None, encode=None):
    files = [f for f in os.listdir('./output') if f.startswith('mail')]
    if files:
        fn = files[-1]+ '1'
    else:
        fn = 'mail'
    writeToFile(output_file_path(fn), message)

def prepareMailSendTest():
    # patch MailHost
    MailBase._send = _send_MH
    if ver == "2.1":
        # patch SecureMailHost
        SecureMailBase.send = send_SMH
        SecureMailBase._send = _send_SMH

def setProperties(prop_sheet, *props):
    for p in ALL_PROPS:
        prop_sheet._updateProperty(p, p in props)

def testMailExistance():
    for f in os.listdir('./output'):
        if f.startswith('mail'):
            return True
    return False

def cleanOutputDir():
    for f in os.listdir('./output'):
        if f.startswith('mail'): os.remove('./output/%s'%f)