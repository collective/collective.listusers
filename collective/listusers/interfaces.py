# -*- coding: utf-8 -*-
"""Module where all interfaces and schemas live."""

from zope.interface import Interface


class IListUsersLayer(Interface):
    """Marker interface for defining a Zope 3 browser layer."""
