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

def addPythonScript(self, out):
    """Add a PythonScript to portal root directory """

    if not hasattr(self, PYTHON_SCRIPT):
        factory = self.manage_addProduct['PythonScripts']
        factory.manage_addPythonScript(PYTHON_SCRIPT)
        script = getattr(self, PYTHON_SCRIPT)
        if script:
            script.ZPythonScript_edit('', 'return context.%s(context)' % EXTERNAL_METHOD)
            out.write('%s python script added to portal\n' % PYTHON_SCRIPT)
        else: out.write('installation procedure could not create python script\n')
    else: out.write('%s python script already exists in portal\n' % PYTHON_SCRIPT)

def install(self):
    """ Product installation """

    out = StringIO()

    # add external method
    addExternalMethod(self, out)

    # add python script
    addPythonScript(self, out)

    return out.getvalue()

def uninstall(self):
    """ Product uninstallation """

    out = StringIO()

    return out.getvalue()