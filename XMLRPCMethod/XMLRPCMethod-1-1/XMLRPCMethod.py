# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Original Code is XMLRPCMethod version 1.0.
#
# The Initial Developer of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Soren Roug, EEA
# Cornel Nitu, Finsiel Romania

""" XMLRPC Method Product

    This product provides support for remote methods.
"""
__version__='$Revision: 1.11 $'[11:-2]
import xmlrpclib, httplib
from base64 import encodestring
from string import split, join, lower, replace
import sys, os, stat, traceback
from cgi import escape
from urllib import splithost, splitpasswd, splittype, splituser
from threading import Thread

from Globals import Persistent, DTMLFile, MessageDialog, HTML
import OFS.SimpleItem, Acquisition
from OFS.Cache import Cacheable
import AccessControl.Role
from OFS.SimpleItem import pretty_tb
from App.Management import Navigation

_marker = []  # Create a new marker object

manage_addXMLRPCMethodForm=DTMLFile('dtml/methodAdd', globals())

def manage_addXMLRPCMethod(self, id, title, remoteurl, function, timeout, REQUEST=None):
    """ Add an external method to a folder

        An addition to the standard object-creation arguments,
        'id' and title, the following arguments are defined:

        method -- The name of the remote method. This can be a
          an ordinary Python function, or a bound method.

        remoteurl -- The URL of the RPC dispatcher to call.
    """
    id=str(id)
    title=str(title)
    remoteurl=str(remoteurl)
    function=str(function)
    timeout=float(timeout)

    i=XMLRPCMethod(id,title,remoteurl,function,timeout)
    self._setObject(id,i)
    return self.manage_main(self,REQUEST)

class XMLRPCMethod(OFS.SimpleItem.Item, Persistent, Acquisition.Explicit,
                     AccessControl.Role.RoleManager, Navigation, Cacheable):
    """ Web-callable functions that encapsulate remote methods.

    """

    meta_type='XMLRPC Method'

    ZopeTime=Acquisition.Acquired
    HelpSys=Acquisition.Acquired

    manage_options=(
        (
        {'label':'Properties', 'action':'manage_main',
         'help':('XMLRPCMethod','XMLRPC-Method_Properties.stx')},
        {'label':'Test', 'action':'',
         'help':('XMLRPCMethod','XMLRPC-Method_Try-It.stx')},
        )
        +OFS.SimpleItem.Item.manage_options
        +AccessControl.Role.RoleManager.manage_options
        +Cacheable.manage_options
        )

    __ac_permissions__=(
        ('View management screens', ('manage_main',)),
        ('Change XMLRPC Methods', ('manage_edit',)),
        ('View', ('__call__','')),
        )

    def __init__(self, id, title, remoteurl, function,timeout):
        self.id=id
        self.manage_edit(title, remoteurl, function,timeout)

    def __setstate__(self,state):
        XMLRPCMethod.inheritedAttribute('__setstate__')(self, state)
        if not hasattr(self,'_timeout'):
            self._timeout = 5.0

    manage_main=DTMLFile('dtml/methodEdit', globals())

    def manage_edit(self, title, remoteurl, function, timeout, REQUEST=None):
        """Change the external method

        See the description of manage_addXMLRPCMethod for a
        description of the arguments 'remoteurl' and 'function'.
        """
        title=str(title)
        remoteurl=str(remoteurl)
        function=str(function)
        timeout=float(timeout)

        self.title=title
        if remoteurl:
            urltype, url = splittype(remoteurl)
        if urltype != "http":
            raise IOError, "Only http scheme supported"

        host, selector = splithost(url)

        if not host: raise IOError, ('http error', 'No host given')

        self._remoteurl = remoteurl
        self._function = function
        self._timeout = timeout
        self.ZCacheable_invalidate()
        if REQUEST:
            message="XMLRPC Method Created."
            return self.manage_main(self,REQUEST,manage_tabs_message=message)

    def __call__(self, *args):
        """ Call an XMLRPC Method """

        __traceback_info__ = args
        # Retrieve the value from the cache.
        keyset = None
        if self.ZCacheable_isCachingEnabled():
            # Strange; I can't just use args
            keyset = { '*':args }
            # Prepare a cache key.
            results = self.ZCacheable_get(keywords=keyset, default=_marker)
            if results is not _marker:
                return results

        ut = RPCThread(self._remoteurl, self._function, args=args)
        ut.start()
        ut.join(self._timeout)

        results = ut.getresult()
        if keyset is not None:
            if results is not None:
                self.ZCacheable_set(results, keywords=keyset)
        return results

    def function(self): return self._function
    def remoteurl(self): return self._remoteurl
    def timeout(self): return self._timeout

class RPCThread(Thread):

    def __init__(self,remoteurl,function,args=()):
        Thread.__init__(self)
        self.args=args
        self.result = None
        self.rpcerror = None
        self.remoteurl = remoteurl
        self.function = function

    def getresult(self):
        if self.rpcerror:
            raise IOError, escape(self.rpcerror)
        else:
            return self.result

    def run(self):
        self.rpcerror = None
        urltype, url = splittype(self.remoteurl)
        if urltype != "http":
            self.rpcerror = "Only http scheme supported"
            raise IOError, "Only http scheme supported"

        host, selector = splithost(url)

        if not host: raise IOError, ('http error', 'No host given')

        user_passwd, host = splituser(host)

        url = "http://"+ host + selector

        if user_passwd:
            server = xmlrpclib.Server(url, BasicAuthTransport(user_passwd))
        else:
            server = xmlrpclib.Server(url)
        f = server.__getattr__(self.function)
        try: res = apply(f,self.args)
        except (xmlrpclib.Fault,xmlrpclib.ProtocolError,xmlrpclib.ResponseError), v:
            self.rpcerror = str(v)
        #raise IOError, escape(self.rpcerror)
        else:    
            self.result = res


class BasicAuthTransport(xmlrpclib.Transport):
    def __init__(self, userpassword=None):
        self.userpassword=userpassword

    def request(self, host, handler, request_body):
        """ issue XML-RPC request """

        h = httplib.HTTP(host)
        h.putrequest("POST", handler)

        # required by HTTP/1.1
        h.putheader("Host", host)

        # required by XML-RPC
        h.putheader("User-Agent", self.user_agent)
        h.putheader("Content-Type", "text/xml")
        h.putheader("Content-Length", str(len(request_body)))

        # basic auth
        if self.userpassword is not None:
            h.putheader("AUTHORIZATION", "Basic %s" % replace(
                encodestring("%s" % (self.userpassword)),
                "\012", ""))
        h.endheaders()

        if request_body:
            h.send(request_body)

        errcode, errmsg, headers = h.getreply()

        if errcode != 200:
            raise xmlrpclib.ProtocolError(
            host + handler,
            errcode, errmsg,
            headers
            )

        return self.parse_response(h.getfile())
