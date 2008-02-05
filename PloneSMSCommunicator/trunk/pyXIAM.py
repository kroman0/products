# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-12-23 11:56:23 +0200 (Fri, 23 Dec 2005) $
# Copyright: quintagroup.com

"""
pyXIAM is module that defines such classes and functions:

    - `SMSsubmitRequest`, this class define SMSsubmitRepuest type and takes responsibility
                          for creating instance of this class and converting it to xml format.

    Methods:

            - `SMSsubmitRequest.genSMS_id`: generate id for message
            - `SMSsubmitRequest.toXML`: convert SMSsubmitRequest instance to xml format
    Functions:

            - `getAllTextFromTag`: return list of text elements that is nested in 'tag_name'

    Exception classes:

        - `DestinatioNumberError`
        - `NoOriginatorError`

"""

__docformat__ = 'restructuredtext'

from DateTime import DateTime
from xml.dom.minidom import *

def getAllTextFromTag(doc, tag_name):
    """
    return list of text elements that is nested in 'tag_name'
     Parameters:

      - `doc`: this parameter must contain xml document
      - `tag_name`: this is the name of needed tag
    """
    text = ''
    result = []
    bad_char = False
    list_tag_elements = doc.getElementsByTagName(tag_name)
    for tag in list_tag_elements:
        list_subelements = tag.getElementsByTagName('*')
        list_subelements.insert(0, tag)
        for element in list_subelements:
            if element.childNodes[0].nodeValue:
                text += element.childNodes[0].nodeValue.strip()
        result.append(text)
        text = ''

    return result

'''def response_message(id):

    doctype = DocumentType(""" xiamSMS SYSTEM "xiamSMSMessage.dtd" """)
    doc = Document()
    doc.appendChild(doctype)

    #create a 'xiamSMS' tag
    xiam_element = doc.createElement("xiamSMS")
    xiam_element.setAttribute("status", "OK")
    doc.appendChild(xiam_element)

    #create a 'submitRequest' tag
    response_element=doc.createElement("submitRsponse")
    response_element.setAttribute("id", id)
    response = doc.createTextNode('XML contained your response messages')
    response_element.appendChild(response)
    xiam_element.appendChild(response_element)

    return doc.toxml()'''

"""class xiamSMS:

    def __init__(self, id, originator, recipients, request, req_time = None, response = None, res_time = None):
        self.id = id
        self.originator = originator
        self.recipients = recipients
        self.request = request
        self.req_time = req_time
        self.response = response
        self.response_status = None
        self.res_time = res_time

    def setOriginator(self, originator):
        setattr(self, 'originator', originator)

    def setRecipients(self, recipients):
        setattr(self, 'recipients', recipients)

    def setRequest(self, request):
        setattr(self, 'request', request)

    def setReq_time(self, req_time):
        setattr(self, 'req_time', req_time)

    def setResponse(self, response):
        setattr(self, 'response', response)

    def setResponse_status(self, response_status):
        setattr(self, 'response_status', response_status)

    def setRes_time(self, res_time):
        setattr(self, 'res_time', res_time)

    def getOriginator(self):
        return getattr(self, 'originator')

    def getRecipients(self):
        return getattr(self, 'recipients')

    def getRequest(self):
        return getattr(self, 'request')

    def getReq_time(self):
        return getattr(self, 'req_time')

    def getResponse(self):
        return getattr(self, 'response')

    def getResponse_status(self):
        return getattr(self, 'response_status')

    def getRes_time(self):
        return getattr(self, 'res_time')"""

class SMSsubmitRequest:
    """
    This class define SMSsubmitRepuest type and takes responsibility
    for creating instance of this class and converting it to xml format.

    Fields:

        - id: sms id
        - originator: contains phone number of message originator
        - destination: contains phone number of destination
        - body: this is the text of your message
    """
    def __init__(self, originator, destination, body):
        self.id = self.genSMS_id()
        self.originator=originator
        self.destination=destination
        self.body=body

    def genSMS_id(self):
        """
        generate id for message
        """
        sms_id = "quinta%s" % DateTime().strftime("%Y%m%d%H%M%S")
        return sms_id

    def toXML(self):
        """
        convert SMSsubmitRequest instance to xml format
        """
        if not self.id:
            id = "quinta5"

        #create a document
        doctype = DocumentType(""" xiamSMS SYSTEM "xiamSMSMessage.dtd" """)
        doc = Document()
        doc.appendChild(doctype)

        #create a 'xiamSMS' tag
        xiam_element = doc.createElement("xiamSMS")
        doc.appendChild(xiam_element)

        #create a 'submitRequest' tag
        request_element=doc.createElement("submitRequest")
        xiam_element.appendChild(request_element)
        request_element.setAttribute("id", self.id)

        #create a 'from' tag
        if not self.originator:
            raise NoOriginatorError("There is no sender number")
        originator_element=doc.createElement("from")
        number=doc.createTextNode(str(self.originator))
        originator_element.appendChild(number)
        request_element.appendChild(originator_element)

        #create a 'to' tag
        if not self.destination:
            raise DestinatioNumberError ("There is no one destination number")
        for pn in self.destination:
            destination_element=doc.createElement("to")
            number=doc.createTextNode(str(pn))
            destination_element.appendChild(number)
            request_element.appendChild(destination_element)

        #create a 'content' tag
        content_element=doc.createElement("content")
        content_element.setAttribute("type", "text")
        body=doc.createTextNode(str(self.body))
        content_element.appendChild(body)
        request_element.appendChild(content_element)

        return doc.toxml(encoding = "UTF-8")

class DestinatioNumberError(Exception):
    pass

class NoOriginatorError(Exception):
    pass