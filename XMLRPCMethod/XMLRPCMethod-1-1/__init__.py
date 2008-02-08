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
# The Original Code is RDFSummary version 1.0.
#
# The Initial Developer of the Original Code is European Environment
# Agency (EEA).  Portions created by EEA are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Soren Roug, EEA

__doc__='''XMLRPC Method Product Initialization
$Id: __init__.py,v 1.2 2003/06/06 13:26:46 finrocvs Exp $'''
__version__='$Revision: 1.2 $'[11:-2]

import XMLRPCMethod

# This is the new way to initialize products.  It is hoped
# that this more direct mechanism will be more understandable.
def initialize(context):

    context.registerClass(
        XMLRPCMethod.XMLRPCMethod,
        constructors=(XMLRPCMethod.manage_addXMLRPCMethodForm,
                       XMLRPCMethod.manage_addXMLRPCMethod),
        icon='xmlrpc.gif',
        )

    context.registerHelp()
    context.registerHelpTitle('Zope Help')
