# -*- coding: utf-8 -*-
"""The List Users view."""

from collective.listusers import ListUsersMessageFactory as _
from collective.listusers.interfaces import IListUsersForm
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form

import logging

logger = logging.getLogger('collective.listusers')


class ListUsersForm(form.Form):
    """The List Users search form based on z3c.form."""

    fields = field.Fields(IListUsersForm)

    label = _(u"List users")

    # don't try to read Plone root for form fields data, this is only mostly
    # usable for edit forms, where you have an actual context
    ignoreContext = True

    @button.buttonAndHandler(_(u"List users!"))
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



class ListUsersView(FormWrapper):
    """A BrowserView to display the ListUsersForm along with it's results."""
    index = ViewPageTemplateFile('listusers.pt')
    form = ListUsersForm

    def __call__(self):
        """Main view method that handles rendering."""
        # Hide the editable border and tabs
        self.request.set('disable_border', True)

        # Prepare display values for the template
        options = {
            'attributes': self.request.get('form.widgets.user_attributes'),
            'users': self.get_users(),
        }
        return super(ListUsersView, self).__call__()

    def get_users(self):
        """Compile a list of users to display with selected user attributes +
        user group membership and username.

        :returns: Selected (+ additional) attributes for listed users
        :rtype: Dictionary of selected users' attributes
        """
        gtool = getToolByName(self.context, 'portal_groups')

        attrs = self.request.get('form.widgets.user_attributes') or []
        groups = self.request.get('form.widgets.groups') or []
        if not (attrs or groups):
            return
        results = {}

        for user in self.get_groups_members(groups):
            result = []
            for attr in attrs:
                if attr == 'username':
                    result.append(user.getId())
                elif attr == 'groups':
                    result.append(", ".join(sorted(gtool.getGroupsForPrincipal(user))))
                elif attr == 'vcard':
                    # Do nothing, we will render the vcard link manually in the
                    # template.
                    pass
                else:
                    result.append(user.getProperty(attr, ''))

            results[user.getId()] = result

        if not results:
            IStatusMessage(self.request).addStatusMessage(_('Search returned no results.'), type="info")

        return results

    def get_groups_members(self, groups):
        """Get a list of users for the selected groups.

        :param groups: List of group ids to get members for
        :type groups: List of strings
        :returns: List of users that are members of these groups
        :rtype: List of user objects
        """
        gtool = getToolByName(self.context, 'portal_groups')

        users = set()
        for group_id in groups:
            group = gtool.getGroupById(group_id)

            if group:
                users.update(group.getGroupMembers())

        return list(users)
