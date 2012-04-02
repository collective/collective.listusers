# -*- coding: utf-8 -*-
"""Interfaces and schemas."""

from collective.listusers import ListUsersMessageFactory as _
from plone.registry.interfaces import IRegistry
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import provider
from zope import schema
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IContextAwareDefaultFactory


### default factories

@provider(IContextAwareDefaultFactory)
def default_user_attributes(context):
    from collective.listusers.interfaces import IListUsersSettings  # circular
    return queryUtility(IRegistry).forInterface(IListUsersSettings).default_user_attributes


def default_settings_user_attributes():
    """use factory to avoid mutable defaults"""
    return ['fullname', 'email', 'groups']


def default_settings_exclude_groups():
    """use factory to avoid mutable defaults"""
    return ['AuthenticatedUsers']


### validators

def validate_vocabulary(value):
    """check if dotted name really is vocabulary"""
    if queryUtility(IVocabularyFactory, value) is None:
        raise Invalid(_(u"Not a vocabulary: %s") % value)
    return True


def must_select_one_constraint(value):
    """Check that at least item was selected."""
    if len(value) == 0:
        raise Invalid(_(u"You need to select at least one value."))
    return True

### interfaces


class IMapUserAttributesToVCardUtility(Interface):
    """Marker interface"""

    def get_vcard_attributes(self, user):
        """List of vcard attributes"""


class IListUsersLayer(Interface):
    """Marker interface for defining a Zope 3 browser layer."""


class IListUsersForm(Interface):
    """Field definition for List Users form."""

    groups = schema.FrozenSet(
        title=_(u'Groups'),
        description=_(u'Select groups from which you want to display users ' \
            'from.'),
        value_type=schema.Choice(
            vocabulary='collective.listusers.vocabularies.FilteredGroups'
        )
    )

    user_attributes = schema.List(
        title=_(u'User attributes'),
        description=_(u'Select which user attributes you want displayed in ' \
            'the results table.'),
        #constraint=must_select_one_constraint,
        value_type=schema.Choice(
            vocabulary='collective.listusers.vocabularies.UserAttributes',
        ),
        defaultFactory=default_user_attributes,
        required=True,
    )

    search_fullname = schema.TextLine(
        title=_(u'Search'),
        required=False,
    )


class IListUsersSettings(Interface):
    """Global settings for the package"""

    # TODO: use FrozenSet once we fix
    # https://github.com/collective/collective.elephantvocabulary/issues/1
    exclude_groups = schema.List(
        title=_(u'What groups to exclude from the product'),
        description=_(u'Select groups that should not show up in widgets or user list table'),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.Groups',
        ),
        defaultFactory=default_settings_exclude_groups,
    )
    filter_by_member_properties_attribute = schema.Choice(
        title=_(u'User property'),
        description=_(u'What member property to filter on based on defined vocabulary'),
        vocabulary='collective.listusers.vocabularies.UserAttributes',
    )
    filter_by_member_properties_vocabulary = schema.DottedName(
        title=_(u'Dotted name to Vocabulary'),
        description=_(u'Select vocabulary used for filtering by member attribute'),
        constraint=validate_vocabulary,
        required=False,
    )
    enable_user_attributes_widget = schema.Bool(
        title=_(u"label_enable_user_attributes_widget",
                default=u"Enable user attributes widget"),
        description=_(u"help_enable_user_attributes_widget",
                default=u"If checked, it will display widget to select user attributes to show in table"),
        required=False,
        default=True,
    )
    default_user_attributes = schema.List(
        title=_(u'Default user attributes'),
        description=_(u'Select which user attributes you want displayed in ' \
            'the results table.'),
        value_type=schema.Choice(
            vocabulary='collective.listusers.vocabularies.UserAttributes',
        ),
        constraint=must_select_one_constraint,
        defaultFactory=default_settings_user_attributes,
    )
    export_csv_attributes = schema.List(
        title=_(u'User attributes to export'),
        value_type=schema.Choice(
            vocabulary='collective.listusers.vocabularies.UserAttributes',
        ),
        constraint=must_select_one_constraint,
        defaultFactory=default_settings_user_attributes,
    )
