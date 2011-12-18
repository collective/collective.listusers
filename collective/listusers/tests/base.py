# -*- coding: utf-8 -*-
"""Module where test layers and test cases live."""

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from Products.CMFCore.utils import getToolByName

import unittest2 as unittest


class ListUsersLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import collective.listusers
        self.loadZCML(package=collective.listusers)
        z2.installProduct(app, 'collective.listusers')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.listusers:default')

        # Login as Manager
        setRoles(portal, TEST_USER_ID, ('Manager',))

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'collective.listusers')


FIXTURE = ListUsersLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="ListUsersLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="ListUsersLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING

    def createUser(self, user_id, properties=None, roles=None, groups=None):
        """Helper method which creates a user with the provided user_id and
        roles and adds him to the provided groups.
        """
        roles = roles or ['Member']
        groups = groups or []
        properties = properties or {}

        portal = self.layer['portal']
        acl_users = getToolByName(portal, 'acl_users')
        gtool = getToolByName(portal, 'portal_groups')
        memberdata = getToolByName(self.portal, 'portal_memberdata')

        acl_users.userFolderAddUser(user_id, 'password', roles, [])
        user = acl_users.getUserById(user_id)

        # Set user properties
        memberdata.wrapUser(user).setMemberProperties(properties)
        #user.setProperties(properties=properties)

        for group_id in groups:
            gtool.addPrincipalToGroup(user_id, group_id)


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
