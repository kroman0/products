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
    result_f = open(f_path,"a")
    result_f.write(text+'\n')
    result_f.close()

def clearFile(f_path):
    result_f = open(f_path,"w")
    result_f.write('')
    result_f.close()

def testMailSend(self, state='approve'):
    result = getFileContent(output_file_path('mail.res'))
    sample = getFileContent(sample_file_path(state+'.mail'))
    # Check headers
    sample_headers = sample.split('\n')[:2]
    for header in sample_headers:
        self.assert_(header in result, "State:'%s'. Header '%s' not present in sended mail" % (state, header) )
    # Check footer
    sample_footer = sample.split('\n')[-2:-1]
    self.assert_(sample_footer[0] in result, "State:'%s'. Footer '%s' not present in sended mail" % (state, sample_footer[0]) )

def testNotMailSend(self, state='approve'):
    result = getFileContent(output_file_path('mail.res'))
    sample = getFileContent(sample_file_path(state+'.mail'))
    # Check headers
    sample_headers = sample.split('\n')[:2]
    del sample_headers[1]
    for header in sample_headers:
        self.assert_(not header in result, "State:'%s'. Header '%s' present in sended mail" % (state, header) )

def testNotMail(self):
    result = getFileContent(output_file_path('mail.res'))
    self.assert_(not result, "Mail was sended")

def _send_MH( self, mfrom, mto, messageText ):
    writeToFile(output_file_path('mail.res'), messageText)

def _send_SMH(self, mfrom, mto, messageText, debug=False):
    writeToFile(output_file_path('mail.res'), messageText)

def send_SMH(self, message, mto=None, mfrom=None, subject=None, encode=None):
    writeToFile(output_file_path('mail.res'), message)

def prepareMailSendTest():
    # patch MailHost
    MailBase._send = _send_MH
    if ver == "2.1":
        # patch SecureMailHost
        SecureMailBase.send = send_SMH
        SecureMailBase._send = _send_SMH
    # clear 'mail.res' file
    clearFile(output_file_path('mail.res'))
    

#########################################################