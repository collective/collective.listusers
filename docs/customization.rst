Customization
=============

VCard attributes
----------------

VCard attributes are generated from this utility.
Interface can be found at :class:`collective.listusers.interfaces.IMapUserAttributesToVCardUtility`
and default implementation at :class:`collective.listusers.browser.vcard.MapUserAttributesToVCardUtility`.

To override, create `overrides.zcml` and configure your own utility providing the interface.

User attribute filter vocabulary
--------------------------------

In control panel, administrator must provide vocabulary upon which user attribute is matched during filtering.

To override, create `overrides.zcml` and configure your own utility providing the interface.

View adapters
-------------

By default the view is registered at /listusers. If you don't like that:

* use http://pypi.python.org/pypi/z3c.unconfigure
* subclass layer marker interface :class:`collective.listusers.interfaces.IListUsersLayer` and register your own adapters

