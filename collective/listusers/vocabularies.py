# -*- coding: utf-8 -*-
"""Definitions of vocabularies."""

from collective.elephantvocabulary import wrap_vocabulary
from collective.listusers.config import MEMBER_PROPERTIES_TO_EXCLUDE
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope.component import getUtility
from zope.interface import implements
from zope.schema import getFieldNames
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class UserAttributesVocabulary(object):
    """Vocabulary factory for user attributes."""
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Build a vocabulary of user attributes. Get them from the
        IUserDataSchemaProvider utility and add additional ones to support
        extra functionality.
        """
        schema_provider = getUtility(IUserDataSchemaProvider)
        schema = schema_provider.getSchema()
        user_attributes = getFieldNames(schema)

        # Add some additional attributes
        user_attributes.insert(0, 'username')
        user_attributes.append('groups')
        user_attributes.append('vcard')
        user_attributes.sort()

        items = [SimpleTerm(attr, attr, attr) for attr in user_attributes
                 if attr not in MEMBER_PROPERTIES_TO_EXCLUDE]

        return SimpleVocabulary(items)


class FilteredGroupsVocabulary(object):
    """Vocabulary factory for user attributes."""
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Build a vocabulary of user attributes. Get them from the
        IUserDataSchemaProvider utility and add additional ones to support
        extra functionality.
        """
        return wrap_vocabulary(
                'plone.app.vocabularies.Groups',
                hidden_terms_from_registry='collective.listusers.interfaces.IListUsersSettings.exclude_groups',
            )(context)


UserAttributesVocabularyFactory = UserAttributesVocabulary()
FilteredGroupsVocabularyFactory = FilteredGroupsVocabulary()
