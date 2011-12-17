# -*- coding: utf-8 -*-
"""Module where all interfaces and schemas live."""

from collective.listusers import ListUsersMessageFactory as _
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema import Choice
from zope.schema import List


class IListUsersLayer(Interface):
    """Marker interface for defining a Zope 3 browser layer."""


def must_select_one_constraint(value):
    """Check that at least item was selected."""
    if len(value) == 0:
        raise Invalid(_(u"You need to select at least one value."))
    return True


class IListUsersForm(Interface):
    """Field definition for List Users form."""

    groups = List(
        title=_(u'Groups'),
        description=_(u'Select groups from which you want to display users' \
            'from. You can select more than one group.'),
        constraint=must_select_one_constraint,
        value_type=Choice(
            vocabulary='plone.app.vocabularies.Groups',
        )
    )

    user_attributes = List(
        title=_(u'User attributes'),
        description=_(u'Select which user attributes you want displayed in' \
            'the results table.'),
        constraint=must_select_one_constraint,
        value_type=Choice(
            vocabulary='collective.listusers.vocabularies.UserAttributes',
        )
    )
