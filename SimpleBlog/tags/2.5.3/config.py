from Products.Archetypes.public import DisplayList

PROJECTNAME = "SimpleBlog"
SKINS_DIR = 'skins'

GLOBALS = globals()
ENABLE_ADSENSE = 1

# deprecated, just here for compatability
DISPLAY_MODE = DisplayList((
    ('full', 'Full'), ('descriptionOnly', 'Description only'), ('titleOnly', 'Title only') ))


# set to 0 if you don't want entries to be folderish
# use at your own risk. this is not fully tested
ENTRY_IS_FOLDERISH = 1


DIGG_TOPICS = DisplayList(( \
     ('apple', 'Technology:Apple') \
    ,('design', 'Technology:Design') \
    ,('gadgets', 'Technology:Gadgets') \
    ,('hardware', 'Technology:Hardware') \
    ,('tech_news', 'Technology:Industry News') \
    ,('linux_unix', 'Technology:Linux/Unix') \
    ,('mods', 'Technology:Mods') \
    ,('programming', 'Technology:Programming') \
    ,('security', 'Technology:Security') \
    ,('software', 'Technology:Software') \
    ,('tech_deals', 'Technology:Tech Deals') \
    ,('space', 'Science:Space') \
    ,('environment', 'Science:Environment') \
    ,('health', 'Science:Health') \
    ,('general_sciences', 'Science:General Sciences') \
    ,('business_finance', 'World & Business:Business Finance') \
    ,('politics', 'World & Business:Political News') \
    ,('political_opinion', 'World & Business:Political Opinion') \
    ,('world_news', 'World & Business:World News') \
    ,('offbeat_news', 'World & Business:Offbeat News') \
    ,('baseball', 'Sports:Baseball') \
    ,('basketball', 'Sports:Basketball') \
    ,('extreme_sports', 'Sports:Extreme Sports') \
    ,('football', 'Sports:Football - US/Canada') \
    ,('golf', 'Sports:Golf') \
    ,('hockey', 'Sports:Hockey') \
    ,('motorsport', 'Sports:Motorsport') \
    ,('soccer', 'Sports:Soccer') \
    ,('tennis', 'Sports:Tennis') \
    ,('other_sports', 'Sports:Other Sports') \
    ,('videos_animation', 'Videos:Animation') \
    ,('videos_comedy', 'Videos:Comedy') \
    ,('videos_educational', 'Videos:Educational') \
    ,('videos_gaming', 'Videos:Gaming') \
    ,('videos_music', 'Videos:Music') \
    ,('videos_people', 'Videos:People') \
    ,('videos_sports', 'Videos:Sports') \
    ,('celebrity', 'Entertainment:Celebrity') \
    ,('movies', 'Entertainment:Movies') \
    ,('music', 'Entertainment:Music') \
    ,('television', 'Entertainment:Television') \
    ,('gaming_news', 'Gaming:Gaming News') \
    ,('playable_web_games', 'Gaming:Playable Web Games') \
)).sortedByValue()
