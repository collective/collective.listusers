# -*- coding: utf-8 -*-
"""Unit and integration tests for collective.listusers vocabularies."""

from collective.listusers.tests.base import IntegrationTestCase
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest2 as unittest


class TestUserAttributesVocabularyIntegration(IntegrationTestCase):
    """Integration tests for the UserAttributes vocabulary."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_vocabulary_default_values(self):
        """Test that the user attributes vocabulary correctly returns user's
        attributes (with some of them excluded in config.py).
        """
        vocabularyFactory = getUtility(
            IVocabularyFactory,
            name=u"collective.listusers.vocabularies.UserAttributes"
        )
        vocabulary = vocabularyFactory(self.portal)
        terms = list(vocabulary)
        expected_attributes = [
            'username',
            'fullname',
            'email',
            'home_page',
            'description',
            'location',
            'groups',
            'vcard',
        ]
        actual_attributes = [term.title for term in terms]
        expected_attributes.sort()
        actual_attributes.sort()

        self.assertEquals(expected_attributes, actual_attributes)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
