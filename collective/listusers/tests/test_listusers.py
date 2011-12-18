# -*- coding: utf-8 -*-
"""Tests for the listusers form and view."""

from collective.listusers.interfaces import IListUsersLayer
from collective.listusers.tests.base import IntegrationTestCase
from zope.component import getMultiAdapter
from zope.interface import directlyProvides

import unittest2 as unittest


class TestListUsersView(IntegrationTestCase):
    """Test the view for listing users."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IListUsersLayer)

        # create some dummy content
        self.createUser('user1', groups=['Administrators'])
        self.createUser('user2', groups=['Reviewers'])
        self.createUser('user3', groups=['Administrators', 'Reviewers'])
        self.createUser('user4', groups=['Site Administrators'])

    def test_view_registration(self):
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )
        self.failUnless(listusers_view)

    def test_get_users(self):
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )
        self.request.form.update({
             'user_attributes': ['fullname', 'email'],
             'groups': ['Administrators']
            }
        )
        self.assertEquals(listusers_view.get_users(), [])


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
