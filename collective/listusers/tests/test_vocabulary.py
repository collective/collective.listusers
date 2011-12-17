# -*- coding: utf-8 -*-
"""Unit and integration tests for StylesVocabulary."""

from collective.listusers.tests.base import IntegrationTestCase
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope.component import getUtility
from zope.component import provideUtility
from zope import schema
from zope.interface import implements
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory

import unittest2 as unittest


class TestVocabularyIntegration(IntegrationTestCase):
    """Integration tests for StylesVocabulary vocabulary that reads values
    from control panel configlet.
    """

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_vocabulary_default_values(self):
        """Integration test to check if the vocabulary correctly returns the
        default user schema."""
        vocabularyFactory = getUtility(
            IVocabularyFactory,
            name=u"collective.listusers.vocabularies.UserAttributes"
        )
        vocabulary = vocabularyFactory(self.portal)
        terms = list(vocabulary)
        expected_attributes = ['fullname', 'email', 'home_page', 'description',
                                'location', 'portrait', 'pdelete']
        actual_attributes = [term.title for term in terms]

        self.assertEquals(expected_attributes.sort(),
                          actual_attributes.sort())


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
