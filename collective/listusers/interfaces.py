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
    """TODO: add docstring"""

    groups = List(
        title=u'Groups',
        constraint=must_select_one_constraint,
        value_type=Choice(
            vocabulary='plone.app.vocabularies.Groups',
        )
    )

    user_attributes = List(
        title=u'User attributes',
        constraint=must_select_one_constraint,
        value_type=Choice(
            vocabulary='collective.listusers.vocabularies.UserAttributes',
        )
    )
