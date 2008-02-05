from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.ShortMessage.config import *
from StringIO import StringIO

from Products.ShortMessage.ShortMessage import ShortMessage
from Products.ShortMessage.Extensions.Sm_Workflow import *

def setPortalFactoryType(self, out,):
    pf=getToolByName(self, 'portal_factory')
    ftypes=list(pf.getFactoryTypes())
    if 'ShortMessage'not in ftypes:
        ftypes.append('ShortMessage')
        pf.manage_setPortalFactoryTypes(listOfTypeIds=ftypes)
    else:
        print >>out, " %s type already  in portal_factory..." %PROJECTNAME

    print >> out, "Set %s type to portal_factory" %PROJECTNAME

def install_workflow(self, out):

    setupWorkflow(self)
    print >> out, "Installed workflow..."

def install(self):

    out=StringIO();

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    setPortalFactoryType(self, out)
    install_workflow(self, out)

#    install_subskin(self, out, GLOBALS)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()
