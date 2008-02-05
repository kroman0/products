from Products.validation.interfaces.IValidator import IValidator

class MaxSmValidator:
    """validator for short message"""

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
	