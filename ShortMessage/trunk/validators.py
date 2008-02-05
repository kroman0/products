# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 13:15:21 +0200 (Thu, 23 Nov 2005) $
# Copyright: quintagroup.com

"""In this module define MaxSmValidator class that validate text block not more then 160 symbols"""

__docformat__ = 'restructuredtext'

from Products.validation.interfaces.IValidator import IValidator

class MaxSmValidator:

    __implements__ = IValidator

    def __init__(self, name = '', maxsize=160, ):
        self.name=name    
        self.maxsize=maxsize
	
    def __call__(self, value, **kwargs):
        sms_size=len(value)
	if kwargs.has_key('maxsize'):
            maxsize = kwargs.get('maxsize')

	maxsize = self.maxsize    

	if sms_size > maxsize:
	    return "Validation failed MaxSmValidator: Typed body is too large: %s (max %s)" % (sms_size, maxsize) 
 	else:
	    return True	     
	