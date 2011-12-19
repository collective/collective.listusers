Search form for listing users
=============================

A Plone 4 add-on to queries users via PAS, user could be from source_users as
well as ldap.

An alphabetical list of groups is to be presented in multiple columns
with checkboxes - multiple can be selected - groups from ldap and/or
source_groups. -- Eventually a multiple select list instead of the
checkboxes.

Below/next to it, the same for a list of values for an attribute. Values
come from a fixed list, customer will hook up to a vocabulary.

A search button.

A clear button.

The output is a table, that needs to support sorting for each
column. Columns are selected user attributes and one column with the
user's groups.

They will themselves register the search form (zcml) where needed.

* `Source code @ GitHub <http://github.com/collective/collective.listusers>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/collective.listusers>`_
* `Sphinx docs @ ReadTheDocs <http://readthedocs.org/docs/collectivelistusers>`_

Installation
============

To install `collective.listusers` you simply add ``collective.listusers``
to the list of eggs in your ``buildout.cfg``, re-run buildout and restart Plone.
Then, install `collective.listusers` using the Add-ons control panel.

