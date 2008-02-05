# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 11:05:50 +0200 (Thu, 23 Nov 2005) $
# Copyright: quintagroup.com

"""
This tool talks to XIAM gateway at cellphone operator
via XIAM-XML protocol. You'd have to set XIAM gateway properties
in the tool' configlet before you are able to send SMSes.
This module defines the following classes:

    - `PloneSMSCommunicator`, this is the tool that carries responsibility for
                              connection with server (message center) and sending via XIAM-XML protocol
                              requests(short message) to server and get responses from it

            Methods:

              - `PloneSMSCommunicator.setProperties`: set PloneSMSCommunicator properties 
              - `PloneSMSCommunicator.getProperties`: return all properties if ids == None, else return properties that in ids list
              - `PloneSMSCommunicator.LOG`: write all needed data to log file
              - `PloneSMSCommunicator.write_sms`: write sms 'in' and sms 'out' files to sms directory
              - `PloneSMSCommunicator.send_Request`: this function will send message to destination
              - `PloneSMSCommunicator.Response`: write all data from response to xiam.log file
              - `PloneSMSCommunicator.getAvailableSMSPolicies`: return sms policies
              - `PloneSMSCommunicator.getServerInfo`: return dictionary that contains host name and ip address
              - `PloneSMSCommunicator.getLogs`: return records from log file


Exception classes:

    - `SendMessageError`

"""
__docformat__ = 'restructuredtext'

from Products.PloneSMSCommunicator.Utils import getHostName
from urllib2 import urlopen, Request, HTTPError, URLError
from Products.Archetypes.public import *
from xml.dom.minidom import *
from StringIO import StringIO
from DateTime import DateTime
from time import strftime
import socket
import os

from config import *
from pyXIAM import *


class SendMessageError(IOError):

    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return '<Can\'t send message because %s>' % self.reason

class PloneSMSCommunicator(BaseFolder):

    _properties = (
      { 'id': 'server_url', 'type':'string', 'mode':'w' },
      { 'id': 'policy', 'type':'selection', 'mode':'w', 'select_variable':'getAvailableSMSPolicies'},
      { 'id': 'mtMessageOriginator', 'type':'string', 'mode':'w' },
      { 'id': 'provider_id', 'type':'string', 'mode':'w' },
      { 'id': 'log_flag', 'type':'boolean', 'mode':'w' },
    )

    archetype_name="PloneSMSCommunicator"
    id=COMMUNICATORID

    def __init__(self):
        BaseFolder.__init__(self, self.id)
        self.server_url = SERVER_URL
        self.policy = 'free'
        self.mtMessageOriginator = ORIGINATOR
        self.log_flag = True
        self.provider_id = PROVIDER

    def setProperties(self, **properties):
        """
        set PloneSMSCommunicator properties
         Parameters:

          -**properties: this is the dictionary that contains pair(property_name: value)
        """
        for property in properties.keys():
            setattr(self, property, properties[property])

    def getProperties(self, ids = []):
        """
        return all properties if ids == None, else return properties that in ids list
        """
        props = {}
        if ids:
            for i in ids:
                props[i] = getattr(self, i)
        else:
            for p in self._properties:
                property = p['id']
                props[property] = getattr(self, property, None)

        return props

    def LOG(self, INFO, data):
        """
        write all needed data to log file
         Parameters:

          - INFO: this is the parameter that defines priority of log data
          - data: all needed data to write
        """
        if self.log_flag:
            log_time = DateTime().strftime("%Y/%m/%d %H:%M:%S")
            xiam_log = file(XIAM_LOG, 'a')
            xiam_log.write(log_time)
            xiam_log.write(data)

    def write_sms(self, sms_id, request = None, response = None):
        """
        write sms 'in' and sms 'out' files to sms directory
         Parameters:

          - sms_id: id of your short message
          - request: this is the data that was sent
          - response: this is the data that was received from server
        """
        if self.log_flag:
            #create sms directory
            if  not 'sms' in os.listdir(CLIENT_HOME):
                 os.mkdir(CLIENT_HOME+'/sms')

            if request:
                sms_request = file(SMS_LOG+sms_id+'out.xml', 'w')
                sms_request.write(request)
                sms_request.close()

            if response:
                sms_response = file(SMS_LOG+sms_id+'in.xml', 'w')
                sms_response.write(response)
                sms_response.close()

    def	send_Request(self, originator, destination, body):
        """
        This function will send message to destination.
         Parameters:

          - originator: contains phone number of message originator
          - destination: contains phone number of destination
          - body: this is the text of your message
        """
        response = StringIO()
        request=SMSsubmitRequest(originator, destination, body)
        xml = str(request.toXML())
        self.write_sms(request.id, request = xml)
        data = Request(self.server_url, xml, headers = {'X-XIAM-Provider-ID':self.provider_id})
        self.LOG('INFO', " > Sent %(id)s request. Originator: %(originator)s, %(noRecipients)d recipients (%(id)sout.xml)\n" % \
            {'id': request.id,
             'originator': originator,
             'noRecipients': len(destination)
            })
        try:
            response = urlopen(data)
            response_status = '200 OK'
        except HTTPError, e:
            response_status = str(e.code)+' '+e.msg
        except URLError, e:
            raise SendMessageError(e)
        str_response = response.read()
        self.write_sms(request.id, response = str_response)
        self.LOG('INFO', " < Received response %(response_status)s (%(id)sin.xml)\n" % \
            {'response_status': response_status,
             'id': request.id
            })
        response.close()

    def Response(self, REQUEST = None):
        """
        write all data from response to xiam.log file
        """
        stream = REQUEST.stdin
        stream.seek(0)
        response_xml = stream.read()
        self.LOG('INFO', response_xml)
        return

    def getAvailableSMSPolicies(self):
        """
        return sms policies
        """
        return ['free', 'enforceOriginator']

    def getServerInfo(self, server_url):
        """
        return dictionary that contains host name and ip address
         Parameters:

          - server_url: url address of server
        """
        info = {}
        info['host_name'] = getHostName(server_url)
        info['ip_addr'] = socket.gethostbyname(info['host_name'])
        return info

    def getLogs(self, size):
        """
        return records from log file
         Parameters:

          - size: number of needed records
        """
        line = ''
        result = []
        xiam_log = file(XIAM_LOG, 'r')
        logs = xiam_log.read()
        for log in logs:
            if log != '\n':
                line = line+log
            else:
                result.append(line)
                line = ''
        result = result[-size:]
        result.reverse()
        return result

registerType(PloneSMSCommunicator)