# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from Products.CMFCore.utils import getToolByName
from collective.listusers.tests.base import IntegrationTestCase

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

    # cssregistry.xml
    def test_css_registered(self):
        """Test if listusers.css file is registered with portal_css."""
        resources = self.portal.portal_css.getResources()
        ids = [r.getId() for r in resources]
        self.failUnless('++resource++collective.listusers/listusers.css' in ids, 'listusers.css not found in portal_css')

    # jsregistry.xml
    def test_js_registered(self):
        """Test if listusers.js file is registered with portal_javascript."""
        resources = self.portal.portal_javascripts.getResources()
        ids = [r.getId() for r in resources]
        self.failUnless('++resource++collective.listusers/listusers.js' in ids, 'listusers.js not found in portal_javascript')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
