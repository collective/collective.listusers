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

In control panel, administrator can provide a vocabulary as base for a user attribute filter widget.


View adapters
-------------

By default the view is registered at /listusers. If you don't like that:

* use http://pypi.python.org/pypi/z3c.unconfigure
* subclass layer marker interface :class:`collective.listusers.interfaces.IListUsersLayer` and register your own adapters

