from Permissions import *
from Products.Archetypes.public import DisplayList

PROJECTNAME = "SimpleBlog"
SKINS_DIR = 'skins'

GLOBALS = globals()

DISPLAY_MODE = DisplayList((
    ('full', 'Full', 'display_full'), 
    ('descriptionOnly', 'Description only', 'display_description_only'), 
    ('titleOnly', 'Title only', 'display_title_only') ))
