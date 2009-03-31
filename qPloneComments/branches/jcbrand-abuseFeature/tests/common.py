#
# Common constants and methods
#

from Products.CMFCore.utils import getToolByName

PRODUCT = 'qPloneComments'
USERS = {# Common Members
         'admin':{'passw': 'secret_admin', 'roles': ['Manager']},
         'owner':{'passw': 'secret_owner', 'roles': ['Owner']},
         'member':{'passw': 'secret_member', 'roles': ['Member']},
         'reviewer':{'passw': 'secret_reviewer', 'roles': ['Reviewer']},
         # Members for discussion manager group
         'dm_admin':{'passw': 'secret_dm_admin', 'roles': ['Manager']},
         'dm_owner':{'passw': 'secret_dm_owner', 'roles': ['Owner']},
         'dm_member':{'passw': 'secret_dm_member', 'roles': ['Member']},
         'dm_reviewer':{'passw': 'secret_dm_reviewer', 'roles': ['Reviewer']},
        }
COMMON_USERS_IDS = [u for u in USERS.keys() if not u.startswith('dm_')]
COMMON_USERS_IDS.append('anonym')
DM_USERS_IDS = [u for u in USERS.keys() if u.startswith('dm_')]

def addMembers(portal, users_map):
    """ Add all members """
    membership = getToolByName(portal, 'portal_membership', None)
    for user_id in users_map.keys():
        membership.addMember(user_id, users_map[user_id]['passw'] , users_map[user_id]['roles'], [], 
                            {'email': '%s@test.com'%user_id,})

def add2Group(portal, group, group_members):
    """ Add users to Discussion Manager group """
    pg = getToolByName(portal, 'portal_groups')
    group = pg.getGroupById(group)
    [group.addMember(u) for u in group_members]
