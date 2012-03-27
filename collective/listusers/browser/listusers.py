# -*- coding: utf-8 -*-
"""The List Users view."""

import logging
import urllib

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

    method = 'get'
    fields = field.Fields(IListUsersForm)

    label = _(u"List users")

    # don't try to read Plone root for form fields data, this is only mostly
    # usable for edit forms, where you have an actual context
    ignoreContext = True

    @button.buttonAndHandler(_(u"List users!"), name="listusers")
    def submit_form(self, action):
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
        self.gtool = getToolByName(self.context, 'portal_groups')

        self.groups = self.request.get('form.widgets.groups') or []
        self.filter_by_member_properties = self.request.get('form.widgets.filter_by_member_properties', [])
        self.search_fullname = self.request.get('form.widgets.search_fullname')

        if self.settings.enable_user_attributes_widget:
            self.user_attributes = self.request.get('form.widgets.user_attributes')
        else:
            self.user_attributes = self.settings.default_user_attributes

        self.options = {
            'attributes': self.user_attributes,
            'users': [],
        }
        # Prepare display values for the template
        if self.request.get('form.buttons.listusers'):
            if not self.user_attributes:
                IStatusMessage(self.request).addStatusMessage(_('No user attributes predefined.'), type="error")
                return

            self.options['users'] = self.get_users()

    def get_users(self):
        """Compile a list of users to display with selected user attributes

        :returns: Selected (+ additional) attributes for listed users
        :rtype: Dictionary of selected users' attributes
        """
        no_users = True
        for user in self.get_groups_members(self.groups):
            no_users = False
            user_data = self.extract_user_data(user)
            if user_data:
                yield user_data

        if no_users:
            IStatusMessage(self.request).addStatusMessage(_('Search returned no results.'), type="info")

    def extract_user_data(self, user):
        """Retrieve dictionary data for template from user object"""
        result = dict()

        # filter by attribute if enabled
        if self.settings.filter_by_member_properties_vocabulary and \
           self.settings.filter_by_member_properties_attribute and \
           self.filter_by_member_properties and \
           user.getproperty(self.settings.filter_by_member_properties_attribute, '') not in self.filter_by_member_properties:
            return

        # do fullname search
        if self.search_fullname and self.search_fullname not in user.getProperty('fullname', '').lower():
            return

        for attr in self.user_attributes:
            if attr in ['username', 'vcard']:
                # Only save the user_id, we will render the vcard link
                # manually in the template.
                result[attr] = user.getId()
            elif attr == 'groups':
                result[attr] = ", ".join(sorted(filter(
                    lambda g: g not in self.settings.exclude_groups, self.gtool.getGroupsForPrincipal(user)
                )))
            else:
                result[attr] = user.getProperty(attr, '')

        return result

    def get_groups_members(self, groups):
        """Get a list of users for the selected groups.

        :param groups: List of group ids to get members for
        :type groups: List of strings
        :returns: List of users that are members of these groups
        :rtype: List of user objects
        """

        if not groups:
            for user in self.context.acl_users.getUsers():
                yield user

        users = set()
        for group_id in groups:
            group = self.gtool.getGroupById(group_id)

            if group:
                users.update(group.getGroupMembers())

        for user in  iter(users):
            yield user


class ListLDAPUsersView(ListUsersView):
    """Implements PAS user search with LDAP batching support"""
    index = ViewPageTemplateFile('listldapusers.pt')

    def get_users(self):
        pasldap = self.context.acl_users.pasldap
        page_size = self.request.get('page_size', 2)
        cookie = self.request.form.get('cookie', '')

        criteria = {}
        if self.search_fullname:
            criteria['fullname'] = self.search_fullname

        for group_id in self.groups:
            criteria.setdefault('memberOf', []).append(
                pasldap.groups[group_id].context.DN
                )

        if self.settings.filter_by_member_properties_vocabulary and \
           self.settings.filter_by_member_properties_attribute and \
           self.filter_by_member_properties:
            criteria[self.settings.filter_by_member_properties_attribute] = self.filter_by_member_properties

        users, cookie = pasldap.users.search(
            criteria=criteria,
            or_keys=False,
            or_values=True,
            attrlist=['fullname'],
            page_size=int(page_size),
            cookie=cookie,
            )
        self.request.form['cookie'] = cookie
        for user in users:
            yield user

    def query_more(self):
        """Get the next page

        It is important that get_users is called first, as that will set the new cookie.
        """
        return '?' + urllib.urlencode(self.request.form, doseq=True)

class ListLDAPUserDetailsView(ListUsersView):
    """Implements PAS user search with LDAP batching support"""
    index = ViewPageTemplateFile('detailsldapusers.pt')

    def update(self):
        """"""
        userid = self.request.get('userid')
        self.options = {}
        self.options['user'] = self.context.acl_users.getUserById(userid)
