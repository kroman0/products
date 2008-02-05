# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 13:10:10 +0200 (Thu, 23 Nov 2005) $
# Copyright: quintagroup.com

"""
This module is created for installing ShortMessage product to Plone site.
 It has such functions:

     - `install`: this function sets all types in ShortMessage product, also install skin directory and other
     - `install_workflow`: this function create new workflow and sets it to ShortMessage type
     - `setPortalFactoryType`: sets ShortMessage type to PortalFactory
"""
__docformat__ = 'restructuredtext'

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.ShortMessage.config import *
from StringIO import StringIO

from Products.ShortMessage.ShortMessage import ShortMessage
from Products.ShortMessage.Extensions.Sm_Workflow import *

def setPortalFactoryType(self, out,):
    """sets ShortMessage type to PortalFactory"""
    pf=getToolByName(self, 'portal_factory')
    ftypes=list(pf.getFactoryTypes())
    if 'ShortMessage'not in ftypes:
        ftypes.append('ShortMessage')
        pf.manage_setPortalFactoryTypes(listOfTypeIds=ftypes)
    else:
        print >>out, " %s type already  in portal_factory..." %PROJECTNAME

    print >> out, "Set %s type to portal_factory" %PROJECTNAME

def install_workflow(self, out):
    """this function create new workflow and sets it to ShortMessage type"""
    setupWorkflow(self)
    print >> out, "Installed workflow..."

def install(self):
    """this function sets all types in ShortMessage product, also install skin directory and other"""
    out=StringIO();

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    setPortalFactoryType(self, out)
    install_workflow(self, out)

#    install_subskin(self, out, GLOBALS)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()
