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

import logging

logger = logging.getLogger('collective.listusers')


class ListUsersForm(form.Form):
    """The List Users form."""

    fields = field.Fields(IListUsersForm)

    label = _(u"List users")

    # don't try to read Plone root for form fields data, this is only mostly
    # usable for edit forms, where you have an actual context
    ignoreContext = True

    @button.buttonAndHandler(_(u"List users"))
    def list_users(self, action):
        """Submit button handler."""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

    @button.buttonAndHandler(_(u"Reset"))
    def reset_form(self, action):
        """Cancel button handler."""
        url = self.context.portal_url() + "/@@listusers"
        self.request.response.redirect(url)


class ListUsersFormWrapper(FormWrapper):
    """Subclass FormWrapper so that we can use a custom frame template that
    renders only the form, nothing else."""
    index = ViewPageTemplateFile("formwrapper.pt")


class ListUsersView(BrowserView):
    """A BrowserView to display the ListUsersForm along with it's results."""
    index = ViewPageTemplateFile('listusers.pt')

    def __init__(self, context, request):
        """Override BrowserView's __init__ to create the ListUsersForm
        for later use."""
        BrowserView.__init__(self, context, request)
        self.form_wrapper = ListUsersFormWrapper(self.context, self.request)
        self.form_wrapper.form_instance = ListUsersForm(self.context, self.request)

    def __call__(self):
        """Main view method that handles rendering."""
        # Hide the editable border and tabs
        self.request.set('disable_border', True)

        # Which user attributes to use
        self.attributes = self.get_attributes()

        # Prepare display values for the template
        options = {
            'attributes': self.attributes,
            'users': self.get_users(),
        }
        return self.index(**options)

    def update(self):
        """This is needed so that KSS validation from plone.app.z3cform works
        as expected."""
        self.form_wrapper.form_instance.update()

    def get_attributes(self):
        """Fetch a list of user attributes."""
        return self.request.get('form.widgets.user_attributes')

    def get_users(self):
        """Compile a list of users to display."""

        # Just a precaution
        if not self.attributes:
            logger.warning('User has not selected any attributes.')
            return []

        # Just a precaution
        if not self.get_group_ids():
            logger.warning('User has not selected any groups.')
            return []

        gtool = getToolByName(self.context, 'portal_groups')
        group_ids = self.get_group_ids()
        users = set()

        # Get users for all the selected groups
        for group_id in group_ids:
            group = gtool.getGroupById(group_id)
            users.update(group.getGroupMembers())

        results = []

        # Results should have only the selected properties
        for user in list(users):
            result = []
            for attr in self.attributes:
                result.append(user.getProperty(attr))
            results.append(result)

        return results
