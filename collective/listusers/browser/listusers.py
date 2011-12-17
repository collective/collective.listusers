# -*- coding: utf-8 -*-
"""Module where the list users form lives."""

from collective.listusers import ListUsersMessageFactory as _
from collective.listusers.interfaces import IListUsersForm
from z3c.form import button
from z3c.form import field
from z3c.form import form


class ListUsersForm(form.Form):
    """The List Users form."""

    fields = field.Fields(IListUsersForm)

    label = _(u"TODO label")
    description = _(u"TODO description")

    # don't try to read Plone root for form fields data, this is only mostly
    # usable for edit forms, where you have an actual context
    ignoreContext = True

    # Hide the editable border and tabs
    def update(self):
        self.request.set('disable_border', True)
        return super(ListUsersForm, self).update()

    @button.buttonAndHandler(_(u"List users"))
    def list_users(self, action):
        """TODO: docstring"""

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        return 'list'

    @button.buttonAndHandler(_(u"Reset"))
    def reset_form(self, action):

        # TODO: clear both form fields
        self.status = _(u"reset.")
        return 'reset'
