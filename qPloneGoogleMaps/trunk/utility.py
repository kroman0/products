
""" Utility module """

def processDesc(desc):
    """ Utility function for processing objects descriptions  """
    import re
    pattern1 = re.compile(r'[\r\n]', re.M|re.I)
    pattern2 = re.compile(r'[\"]', re.M|re.I)
    res = pattern2.sub("'", desc)
    return pattern1.sub(' ', res)