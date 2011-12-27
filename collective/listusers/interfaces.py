# -*- coding: utf-8 -*-
"""Interfaces and schemas."""

from collective.listusers import ListUsersMessageFactory as _
from plone.registry.interfaces import IRegistry
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import provider
from zope import schema
from zope.component import queryUtility
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def default_user_attributes(context):
    from collective.listusers.interfaces import IListUsersSettings  # circular
    return queryUtility(IRegistry).forInterface(IListUsersSettings).default_user_attributes


def must_select_one_constraint(value):
    """Check that at least item was selected."""
    if len(value) == 0:
        raise Invalid(_(u"You need to select at least one value."))
    return True


class IListUsersLayer(Interface):
    """Marker interface for defining a Zope 3 browser layer."""


class IListUsersForm(Interface):
    """Field definition for List Users form."""

    groups = schema.FrozenSet(
        title=_(u'Groups'),
        description=_(u'Select groups from which you want to display users ' \
            'from.'),
        constraint=must_select_one_constraint,
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


class IListUsersSettings(Interface):
    """Global settings for the package"""

    exclude_groups = schema.List(  # TODO: use FrozenSet once we fix https://github.com/collective/collective.elephantvocabulary/issues/1
        title=_(u'What groups to exclude from the product'),
        description=_(u'Select groups that should not show up in widgets or user list table'),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.Groups',
        ),
        default=list(('AuthenticatedUsers',)),
    )
    filter_by_member_properties_vocabulary = schema.DottedName(
        title=_(u'Dotted name to Vocabulary'),
        description=_(u'Select vocabulary used for filtering by member attribute'),
        required=False,
    )
    filter_by_member_properties_attribute = schema.Choice(
        title=_(u'User property'),
        description=_(u'What member property to filter on based on defined vocabulary'),
        vocabulary='collective.listusers.vocabularies.UserAttributes',
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
        #constraint=must_select_one_constraint,
        default=list(('username', 'fullname')),
    )
