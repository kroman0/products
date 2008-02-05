import os
from Globals import package_home

from Products.CMFPlone import cmfplone_globals
path = os.path.join(package_home(cmfplone_globals))
files=os.listdir(path)
for f in files:
    if f.lower()=='version.txt':
        version = open(os.path.join(path,f)).read().strip()
        if version.startswith('2.0.'):
            import patch_del_members, patch_portraits
        elif version.strip() in ('2.1.1', '2.1.2', '2.1.3', '2.5'):
            import patch_portraits

