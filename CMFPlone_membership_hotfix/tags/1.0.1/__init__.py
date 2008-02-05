import os
from Globals import package_home

try:
    from Products.CMFPlone import cmfplone_globals
    path = os.path.join(package_home(cmfplone_globals))
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

