# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2006-08-11 
# Copyright: quintagroup.com

from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from types import InstanceType

from Products.qPloneResolveUID.config import *

def registerTransform(self, out, name, module):
    transforms = getToolByName(self, 'portal_transforms')
    transforms.manage_addTransform(name, module)
    print >> out, "Registered transform", name

def registerTransformPolicy(self, out, output_mimetype, required_transforms):
    transforms = getToolByName(self, 'portal_transforms')
    transforms.manage_addPolicy(output_mimetype, required_transforms)
    print >> out, "Registered policy for %s mimetype" %output_mimetype
    
def unregisterTransform(self, out, name):
    transforms = getToolByName(self, 'portal_transforms')
    try:
        transforms.unregisterTransform(name)
        print >> out, "Removed transform", name
    except AttributeError:
        print >> out, "Could not remove transform", name, "(not found)"

def unregisterTransformPolicy(self, out, output_mimetypes):
    transforms = getToolByName(self, 'portal_transforms')
    transforms.manage_delPolicies(output_mimetypes)
    print >> out, "Removed transform policy for %s mimetype" %output_mimetypes
    
def install(self):

    out = StringIO()

    print >> out, "Installing ruid_to_url transform"
    registerTransform(self, out, 'ruid_to_url', 'Products.qPloneResolveUID.transforms.ruid_to_url')
    
    print >> out, "Installing transform policy for %s mimetype" %DOCUMENT_DEFAULT_OUTPUT_TYPE
    registerTransformPolicy(self, out, DOCUMENT_DEFAULT_OUTPUT_TYPE, REQUIRED_TRANSFORM)
    
    return out.getvalue()

def uninstall(self):

    out = StringIO()
    
    unregisterTransform(self, out, 'ruid_to_url')
    
    print >> out, "Removing transform policy for %s mimetype" %DOCUMENT_DEFAULT_OUTPUT_TYPE
    unregisterTransformPolicy(self, out, [DOCUMENT_DEFAULT_OUTPUT_TYPE,])
    
    return out.getvalue()