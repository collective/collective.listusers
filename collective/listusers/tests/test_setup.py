# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.listusers.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName

import unittest2 as unittest


class TestSetup(IntegrationTestCase):
    """Test installation of collective.listusers into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.listusers is installed with
        portal_quickinstaller.
        """
        self.failUnless(self.installer.isProductInstalled('collective.listusers'))

    def test_dependencies_installed(self):
        """Test that all dependencies are installed."""
        self.failUnless(self.installer.isProductInstalled('collective.js.datatables'))

    def test_uninstall(self):
        """Test if collective.listusers is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.listusers'])
        self.failIf(self.installer.isProductInstalled('collective.listusers'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IListUsersLayer is registered."""
        from collective.listusers.interfaces import IListUsersLayer
        from plone.browserlayer import utils
        self.failUnless(IListUsersLayer in utils.registered_layers())


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
