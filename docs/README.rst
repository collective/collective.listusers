=============================
Search form for listing users
=============================

Search form queries users via PAS, user could be from source_users as
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

AJAX would be great, but not mandatory.

They will themselves register the search form (zcml) where needed.