# -*- coding: utf-8 -*-
"""Module that displays the List Users form."""

from collective.listusers import ListUsersMessageFactory as _
from collective.listusers.interfaces import IListUsersForm
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
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

    @button.buttonAndHandler(_(u"List users"))
    def list_users(self, action):
        """TODO: docstring"""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

    @button.buttonAndHandler(_(u"Reset"))
    def reset_form(self, action):
        """TODO: docstring"""
        url = self.context.portal_url() + "/@@listusers"
        self.request.response.redirect(url)


class ListUsersFormWrapper(FormWrapper):
    """Subclass FormWrapper so that we can use a custom frame template."""
    index = ViewPageTemplateFile("formwrapper.pt")
    form = ListUsersForm


class ListUsersView(BrowserView):
    """A BrowserView to the ListUsersForm along with it's results."""
    index = ViewPageTemplateFile('listusers.pt')

    def __call__(self):

        # Hide the editable border and tabs
        self.request.set('disable_border', True)

        self.attributes = self.get_attributes()

        options = {
            'attributes': self.attributes,
            'users': self.get_users(),
        }
        self.form_wrapper = ListUsersFormWrapper(self.context, self.request)
        return self.index(**options)

    def get_attributes(self):
        """TODO: docstring"""
        return self.request.get('form.widgets.user_attributes')

    def get_users(self):
        """TODO: write docstring"""

        if not self.attributes:
            return []

        acl = getToolByName(self.context, 'acl_users')

        results = []
        for user in acl.getUsers():
            result = []
            for attr in self.attributes:
                result.append(user.getProperty(attr))
            results.append(result)

        for i in range(1, 10):
            results = results + results
        return results
