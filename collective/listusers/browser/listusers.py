# -*- coding: utf-8 -*-
"""The List Users view."""

import logging

from collective.listusers import ListUsersMessageFactory as _
from collective.listusers.interfaces import IListUsersForm, IListUsersSettings
from plone.registry.interfaces import IRegistry
from plone.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.field import Fields
from zope import schema
from zope.component import queryUtility


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

    def updateWidgets(self):
        """Hook before rendering the form"""
        settings = queryUtility(IRegistry).forInterface(IListUsersSettings)

        # filter by user attribute
        if settings.filter_by_member_properties_vocabulary and settings.filter_by_member_properties_attribute:
            field = schema.FrozenSet(
                __name__="filter_by_member_properties",
                title=u"%s" % settings.filter_by_member_properties_attribute.capitalize(),
                description=_(u'Filter members by attribute "%s"') % settings.filter_by_member_properties_attribute,
                value_type=schema.Choice(
                    vocabulary=settings.filter_by_member_properties_vocabulary,
                ),
            )
            self.fields += Fields(field)

        super(ListUsersForm, self).updateWidgets()
        if not settings.enable_user_attributes_widget:
            del self.widgets['user_attributes']


class ListUsersView(FormWrapper):
    """A BrowserView to display the ListUsersForm along with it's results."""
    index = ViewPageTemplateFile('listusers.pt')
    form = ListUsersForm

    def update(self):
        """Main view method that handles rendering."""
        super(ListUsersView, self).update()
        # Hide the editable border and tabs
        self.settings = queryUtility(IRegistry).forInterface(IListUsersSettings)
        self.request.set('disable_border', True)

        if self.settings.enable_user_attributes_widget:
            self.user_attributes = self.request.get('form.widgets.user_attributes')
        else:
            self.user_attributes = self.settings.default_user_attributes

        # Prepare display values for the template
        self.options = {
            'attributes': self.user_attributes,
            'users': self.get_users(),
        }

    def get_users(self):
        """Compile a list of users to display with selected user attributes +
        user group membership and username.

        :returns: Selected (+ additional) attributes for listed users
        :rtype: Dictionary of selected users' attributes
        """
        gtool = getToolByName(self.context, 'portal_groups')

        attrs = self.user_attributes
        groups = self.request.get('form.widgets.groups') or []
        search_fullname = self.request.get('form.widgets.search_fullname', '')
        if not (attrs or groups):
            return

        if not attrs:
            IStatusMessage(self.request).addStatusMessage(_('No user attributes predefined.'), type="error")
            return
        results = {}

        for user in self.get_groups_members(groups):
            result = dict()

            # do fullname search
            if search_fullname and search_fullname not in user.getProperty('fullname', ''):
                continue

            for attr in attrs:
                if attr == 'username':
                    result[attr] = user.getId()
                elif attr == 'groups':
                    result[attr] = ", ".join(sorted(filter(lambda g:
                        g not in self.settings.exclude_groups,
                        gtool.getGroupsForPrincipal(user))))
                elif attr == 'vcard':
                    # Only save the user_id, we will render the vcard link
                    # manually in the template.
                    result[attr] = user.getId()
                else:
                    result[attr] = user.getProperty(attr, '')

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

        # TODO: better way to search for users
        users = set()
        for group_id in groups:
            group = gtool.getGroupById(group_id)

            if group:
                users.update(group.getGroupMembers())

        # filter further by attribute if enabled
        if self.settings.filter_by_member_properties_vocabulary and self.settings.filter_by_member_properties_attribute:
            values = self.request.get('form.widgets.filter_by_member_properties', None)
            attr = self.settings.filter_by_member_properties_attribute
            if values:
                return filter(lambda u: u.getProperty(attr, '') in values, users)
        return list(users)
