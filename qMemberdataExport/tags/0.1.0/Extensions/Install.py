from cStringIO import StringIO

from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod

from Products.CMFCore.utils import getToolByName

from Products.qMemberdataExport.config import *

def addExternalMethod(self, out):
    """ Add external method to portal root directory """

    if not hasattr(self, EXTERNAL_METHOD):
        manage_addExternalMethod(self,
                                id=EXTERNAL_METHOD,
                                title=EXTERNAL_METHOD,
                                module=PROJECTNAME+'.'+'getMemberData',
                                function='getMemberData')
        method = getattr(self, EXTERNAL_METHOD)
        if method:
            method.manage_permission('View', ['Manager',], acquire=0)
            out.write('%s external method added to portal\n' % EXTERNAL_METHOD)
        else: out.write('installation procedure could not create external method\n')
    else: out.write('%s external method already exists in portal\n' % EXTERNAL_METHOD)

def install(self):
    """ Product installation """

    out = StringIO()

    # add external method
    addExternalMethod(self, out)

    return out.getvalue()

def uninstall(self):
    """ Product uninstallation """

    out = StringIO()

    return out.getvalue()