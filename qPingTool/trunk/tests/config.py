# for testPropertiesToolConf
nt_properties = (("metaTypesNotToList", "lines", ["PingTool"]), )

s_properties = (("use_folder_tabs", "lines", ["PingTool"]),
                ("typesLinkToFolderContentsInFC", "lines", ["PingTool"]),
                ("typesUseViewActionInListings", "lines", ["PingInfo"]),)


# for test_skin_installed
skins_content = ['ping_now', 'ping_setup', 'save_ping_setup', 'tool.gif']

# for test_installedAllTypes
istalled_types = ['PingTool', 'PingInfo']

# for test_added_action
types_actions = ({'type':'PingTool', 'actions':(('view', 'View', 'string:folder_contents', ('Manage portal',), 'object', True),)},)
