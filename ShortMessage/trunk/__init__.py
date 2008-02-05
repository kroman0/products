# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 13:10:22 +0200 (Thu, 23 Nov 2005) $
# Copyright: quintagroup.com

"""
This is the init module for ShortMessage product that will initialize all
types in product.
"""
__docformat__ = 'restructuredtext'

from Products.Archetypes.public import *
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from config import *


def initialize(context):

    import ShortMessage

    content_types, constructors, ftis = process_types(
                   listTypes(PROJECTNAME),
                   PROJECTNAME)

    utils.ContentInit(
                PROJECTNAME ,
                content_types      = content_types,
                permission         = ADD_CONTENT_PERMISSION,
                extra_constructors = constructors,
                fti                = ftis,
                ).initialize(context)