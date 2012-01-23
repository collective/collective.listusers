Solves easy task: Query users by group and/or attribute and export as vcard/csv.

Features
========

* query list of users by groups displayed in table
* control panel settings
* configurable exported user attributes
* export listing to csv, vcard
* optional filtering by user attribute hooked to an vobabulary
* z3c.form for widget


Installation
============

#. add `collective.listusers` to the list of eggs in your `buildout.cfg`
#. re-run buildout and restart Plone.
#. install `collective.listusers` using the Add-ons control panel.


Usage
=====


* View gets title information from context, so access it anywhere like http://localhost:8080/Plone/folder-1/@@listusers.
* There is custom permission 'collective.listusers: List users' which needs to be assigned to role/group to access the view.
* Before usage be sure to check configuration options in control panel under addons.
