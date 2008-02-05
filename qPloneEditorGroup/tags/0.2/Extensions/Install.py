from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin 
from Products.CMFCore import CMFCorePermissions 
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def install(self):
    """ install product """
    out = StringIO()
    portal = getToolByName(self,'portal_url').getPortalObject()
    acl = self.acl_users
    try:
        portal._addRole('Editor')
    except KeyError:
        pass
    if acl.meta_type != 'Pluggable Auth Service':
        acl.changeOrCreateGroups(roles = ['Editor'], new_groups=['Editors'])
    else:
        from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
        from Products.PluggableAuthService.interfaces.plugins import IRoleEnumerationPlugin
        plugins = acl._getOb( 'plugins' )
        roles = plugins.listPlugins(IRolesPlugin)
        enumerators = plugins.listPlugins(IRoleEnumerationPlugin)
        role_enums = set(roles) and set(enumerators)

        ids = []
        for rp in role_enums:
            all_roles = rp[1].enumerateRoles()
            ids += [a['id'] for a in all_roles]
        if 'Editor' not in ids:
            acl.addRole('Editor')

        if 'Editors' not in acl.getGroupIds():
            acl._doAddGroup('Editors', roles = ('Editor',))

    out.write('Added Editors group and Editor role\n')

    wt = getToolByName(portal, 'portal_workflow')
    fflow = wt.folder_workflow
    pflow = wt.plone_workflow

    for name, state in fflow.states.items():
        for p in state.getManagedPermissions():
            info = state.getPermissionInfo(p)
            state.setPermission(p, info['acquired'], tuple(info['roles'])+('Editor',))

    for name, state in pflow.states.items():
        for p in state.getManagedPermissions():
            info = state.getPermissionInfo(p)
            state.setPermission(p, info['acquired'], tuple(info['roles'])+('Editor',))

    return out.getvalue()
