#
# Monkey Patch file to allow zope to marshal Zope DateTime objects into
# xml-rpc DateTime objects
#
#######################################################################
import xmlrpclib
import DateTime as ZopeDateTime

def encodeZopeDateTime(self, out):
    dtObj = xmlrpclib.DateTime('%s%02d%02dT%02d:%02d:%02d' % self.parts()[:-1])
    dtObj.encode(out)

ZopeDateTime.DateTime.encode = encodeZopeDateTime

xmlrpclib.WRAPPERS += (ZopeDateTime.DateTime,)
