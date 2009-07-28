from plone.app.registry.browser import controlpanel

from quintagroup.dropdownmenu.interfaces import IDropDownMenuSettings, _


class DropDownMenuSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IDropDownMenuSettings
    label = _(u"DropDown Menu settings")
    description = _(u"Please enter the options specified")


class DropDownMenuSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DropDownMenuSettingsEditForm
