# -*- coding: utf-8 -*-
"""Module where all interfaces and schemas live."""

from zope.interface import Interface
import zope.schema


class IListUsersLayer(Interface):
    """Marker interface for defining a Zope 3 browser layer."""


class IListUsersForm(Interface):
    """TODO: add docstring"""

    groups = zope.schema.List(
        title=u'Groups',
        value_type=zope.schema.Choice(
            vocabulary='plone.app.vocabularies.Groups',
            required=False)
    )

    user_attributes = zope.schema.List(
        title=u'User attributes',
            value_type=zope.schema.Choice(
                vocabulary='collective.listusers.vocabularies.UserAttributes',
                required=False)
    )
