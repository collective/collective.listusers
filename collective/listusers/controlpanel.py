from plone.app.registry.browser import controlpanel

from collective.listusers.interfaces import IListUsersSettings, _


class ListUsersSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IListUsersSettings
    label = _(u"collective.listusers settings")
    description = _(u"""""")

#    def updateFields(self):
#        super(AkismetSettingsEditForm, self).updateFields()

#    def updateWidgets(self):
#        super(AkismetSettingsEditForm, self).updateWidgets()


class ListUsersSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ListUsersSettingsEditForm
