# -*- coding: utf-8 -*-
"""Module that displays the List Users form."""

from collective.listusers import ListUsersMessageFactory as _
from collective.listusers.interfaces import IListUsersForm
from z3c.form import button
from z3c.form import field
from z3c.form import form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ListUsersForm(form.Form):
    """The List Users form."""

    fields = field.Fields(IListUsersForm)

    label = _(u"TODO label")
    description = _(u"TODO description")

    # don't try to read Plone root for form fields data, this is only mostly
    # usable for edit forms, where you have an actual context
    ignoreContext = True

    # Hide the editable border and tabs
    def update(self):
        self.request.set('disable_border', True)
        return super(ListUsersForm, self).update()

    @button.buttonAndHandler(_(u"List users"))
    def list_users(self, action):
        """TODO: docstring"""

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.status = _(u"list")
        return 'list'

    @button.buttonAndHandler(_(u"Reset"))
    def reset_form(self, action):

        # TODO: clear both form fields
        self.status = _(u"reset")
        return 'reset'


from plone.z3cform.layout import FormWrapper


class PortletFormView(FormWrapper):
    """ Form view which renders z3c.forms embedded in a portlet.

    Subclass FormWrapper so that we can use custom frame template. """

    index = ViewPageTemplateFile("formwrapper.pt")


class ListUsersView(BrowserView):
    """A BrowserView to the ListUsersForm along with it's results."""
    index = ViewPageTemplateFile('listusers.pt')

    def __call__(self):
        options = {
            'title': self.request.get('form.widgets.title', None),
        }
        self.form_wrapper = self.getForm()
        return self.index(**options)

    def getForm(self):
        """ Create a form instance.

        @return: z3c.form wrapped for Plone 4 view
        """

        context = self.context.aq_inner

        # returnURL = self.context.absolute_url()

        # Create a compact version of the contact form
        # (not all fields visible)
        #form = ListUsersForm(context, self.request, returnURLHint=returnURL, full=False)
        form = ListUsersForm(context, self.request)

        # Wrap a form in Plone view
        view = PortletFormView(context, self.request)
        view = view.__of__(context)  # Make sure acquisition chain is respected
        view.form_instance = form

        return view
