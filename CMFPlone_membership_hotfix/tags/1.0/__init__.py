import os
from Globals import package_home
from Products.CMFPlone.config import *

try:
    from Products.CMFPlone import plone_globals
    path = os.path.join(package_home(plone_globals))
    try:
        files=os.listdir(path)
        for f in files:
            if f.lower()=='version.txt':
                version = open(os.path.join(path,f)).read().strip()
                if version.startswith('2.0.'):
                    import patch
    except:
        pass
except:
    pass

