# for testPropertiesToolConf
nt_properties = (("metaTypesNotToList", "lines", ["PingTool", "PingInfo"]), )

s_properties = (("use_folder_tabs", "lines", ["PingTool"]),
                ("typesLinkToFolderContentsInFC", "lines", ["PingTool"]),
                ("typesUseViewActionInListings", "lines", ["PingInfo"]),)

# for test_skin_installed
skins_content = ['tool.gif']

# for test_installedAllTypes
istalled_types = ['PingTool', 'PingInfo']

# for test_added_action
types_actions = ({'type':'PingTool',
                  'actions':(('view', 'View', 'string:${object_url}/view', ('Manage portal', ), 'object', True),
                             ('edit', 'Edit', 'string:${object_url}/edit', ('Modify portal content', ), 'object', True),
                            ),
                 },
                 {'type':'PingInfo',
                  'actions':(('view', 'View', 'string:${object_url}/view', ('View',), 'object', True),
                             ('edit', 'Edit', 'string:${object_url}/edit', ('Modify portal content', ), 'object', True),
                             ('metadata', 'Properties', 'string:${object_url}/properties', ('Modify portal content', ), 'object', True),
                             ('references', 'References', 'string:${object_url}/reference_graph', ('Modify portal content', 'Review portal content'), 'object', True),
                            ),
                 },
                )
