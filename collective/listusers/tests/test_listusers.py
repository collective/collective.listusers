# -*- coding: utf-8 -*-
"""Tests for the listusers form and view."""

from collective.listusers.interfaces import IListUsersLayer
from collective.listusers.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName
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
        user1_props = {
            'fullname':'User 1',
            'description': 'User 1 description',
            'email': 'user1@user1.com',
            'location': 'Jupiter',
        }
        user2_props = {
            'fullname':'User 2',
            'description': 'User 2 description',
            'email': 'user2@user2.com',
            'location': 'Moon',
        }
        user3_props = {
            'fullname':'User 3',
            'description': 'User 3 description',
            'email': 'user3@user3.com',
            'location': 'Saturn',
        }
        user4_props = {
            'fullname':'User 4',
            'description': 'User 4 description',
            'email': 'user4@user4.com',
            'location': 'Pluto',
        }
        self.createUser(
            'user1',
            properties=user1_props,
            groups=['Administrators']
        )
        self.createUser(
            'user2',
            properties=user2_props,
            groups=['Reviewers']
        )
        self.createUser(
            'user3',
            properties=user3_props,
            groups=['Administrators', 'Reviewers']
        )
        self.createUser(
            'user4',
            properties=user4_props,
            groups=['Site Administrators']
        )

    def test_view_registration(self):
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )
        self.failUnless(listusers_view)

    def test_get_groups_members(self):
        acl_users = getToolByName(self.portal, 'acl_users')
        memberdata = getToolByName(self.portal, 'portal_memberdata')
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )

        # Test empty groups
        groups = []
        self.assertEquals(listusers_view.get_groups_members(groups), [])

        # Test single group
        groups = ['Site Administrators']
        expected_results = [
            memberdata.wrapUser(acl_users.getUserById('user4')),
        ]
        actual_results = listusers_view.get_groups_members(groups)
        self.assertEquals(actual_results, expected_results)

        # Test multiple groups
        groups = ['Administrators', 'Reviewers']
        expected_results = [
            memberdata.wrapUser(acl_users.getUserById('user1')),
            memberdata.wrapUser(acl_users.getUserById('user2')),
            memberdata.wrapUser(acl_users.getUserById('user3'))
        ]
        actual_results = listusers_view.get_groups_members(groups)
        self.assertEquals(actual_results, expected_results)

    def test_get_users(self):
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )
        self.request.form.update({
             'form.widgets.user_attributes': ['fullname', 'email'],
             'form.widgets.groups': ['Administrators']
            }
        )
        results = {
            'user1': ['User 1', 'user1@user1.com'],
            'user3': ['User 3', 'user3@user3.com']
        }
        # Doesn't work, because the properties aren't properly set
        # check createUser method in base.py
        self.assertEquals(listusers_view.get_users(), results)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
