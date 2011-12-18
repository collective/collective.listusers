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
        self.createUser(
            'user1',
            properties={
                'fullname': 'User 1',
                'description': 'User 1 description',
                'email': 'user1@user1.com',
                'location': 'Jupiter',
            },
            groups=['Administrators']
        )
        self.createUser(
            'user2',
            properties={
                'fullname': 'User 2',
                'description': 'User 2 description',
                'email': 'user2@user2.com',
                'location': 'Moon',
            },
            groups=['Reviewers']
        )
        self.createUser(
            'user3',
            properties={
                'fullname': 'User 3',
                'description': 'User 3 description',
                'email': 'user3@user3.com',
                'location': 'Saturn',
            },
            groups=['Administrators', 'Reviewers']
        )
        self.createUser(
            'user4',
            properties={
                'fullname': 'User 4',
                'description': 'User 4 description',
                'email': 'user4@user4.com',
                'location': 'Pluto',
            },
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
        # Here we check if we got the right results by comparing user ids, not
        # the returned MemberData objects, because it would be difficult
        # to sort them.
        groups = ['Administrators', 'Reviewers']
        expected_results = ['user1', 'user2', 'user3']
        expected_results.sort()
        actual_results = listusers_view.get_groups_members(groups)
        actual_results = [mdata.getId() for mdata in actual_results]
        actual_results.sort()

        self.assertEquals(actual_results, expected_results)

    def test_get_users_empty_attributes(self):
        self.request.form.update({
             'form.widgets.user_attributes': [],
             'form.widgets.groups': ['Administrators']
            }
        )
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )

        self.assertEquals(listusers_view.get_users(), None)

    def test_get_users_nonexistent_attributes(self):
        self.request.form.update({
             'form.widgets.user_attributes': ['home_page'],
             'form.widgets.groups': ['Administrators']
            }
        )
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )
        expected_results = {'user3': [''], 'user1': ['']}

        self.assertEquals(listusers_view.get_users(), expected_results)

    def test_get_users_empty_groups(self):
        self.request.form.update({
             'form.widgets.user_attributes': ['fullname', 'email'],
             'form.widgets.groups': []
            }
        )
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )

        self.assertEquals(listusers_view.get_users(), None)

    def test_get_users_nonexistent_groups(self):
        self.request.form.update({
             'form.widgets.user_attributes': ['fullname', 'email'],
             'form.widgets.groups': ['Non-existent group']
            }
        )
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )

        self.assertEquals(listusers_view.get_users(), {})

    def test_get_users_empty_groups_and_attributes(self):
        self.request.form.update({
             'form.widgets.user_attributes': [],
             'form.widgets.groups': []
            }
        )
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )

        self.assertEquals(listusers_view.get_users(), None)

    def test_get_users_single_group_multiple_attributes(self):
        self.request.form.update({
             'form.widgets.user_attributes': ['fullname', 'email'],
             'form.widgets.groups': ['Administrators']
            }
        )
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )
        expected_results = {
            'user1': ['User 1', 'user1@user1.com'],
            'user3': ['User 3', 'user3@user3.com']
        }

        self.assertEquals(listusers_view.get_users(), expected_results)

    def test_get_users_multiple_groups_and_attributes(self):
        self.request.form.update({
             'form.widgets.user_attributes': ['fullname', 'email', 'location'],
             'form.widgets.groups': ['Administrators', 'Site Administrators']
            }
        )
        listusers_view = getMultiAdapter(
            (self.portal, self.request), name=u'listusers'
        )
        expected_results = {
            'user1': ['User 1', 'user1@user1.com', 'Jupiter'],
            'user3': ['User 3', 'user3@user3.com', 'Saturn'],
            'user4': ['User 4', 'user4@user4.com', 'Pluto']
        }

        self.assertEquals(listusers_view.get_users(), expected_results)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
