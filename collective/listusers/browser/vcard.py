"""VCard view."""

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.component import getUtility

from collective.listusers.interfaces import IMapUserAttributesToVCardUtility


VCARD_TEMPLATE = """BEGIN:VCARD
%s
END:VCARD
"""


class VCardView(BrowserView):
    """View for generating user information in the vcard format."""

    def __call__(self, user_id=None):
        """Main view method that returns vcard info for a given user.

        :returns: vcard info for a given user
        :rtype: vcard format
        """
        if not user_id:
            return

        acl_users = getToolByName(self.context, 'acl_users')
        user = acl_users.getUserById(user_id)

        if hasattr(self, 'get_vcard_attributes'):
            attributes = self.get_vcard_attributes(user)
        else:
            attributes = getUtility(IMapUserAttributesToVCardUtility)().get_vcard_attributes(user)

        vcard = VCARD_TEMPLATE % '\n'.join(attributes)

        self.request.response.setHeader('Content-Type', 'text/vcard')
        self.request.response.setHeader(
            "Content-disposition",
            "attachment;filename=%s.vcf" % user.getId()
        )

        return vcard

class MapUserAttributesToVCardUtility(object):
    """Utility mapping user attributes to vcard output"""
    implements(IMapUserAttributesToVCardUtility)

    def get_vcard_attributes(self, user):
        return (
            "FN:%s" % user.getProperty('fullname', ''),
            "N:%s" % user.getProperty('fullname', ''),
            "ORG:%s" % user.getProperty('organization', ''),
            "ADR:%s;%s" % (user.getProperty('location', ''), user.getProperty('location', '')),
            "TEL;type=WORK:%s" % user.getProperty('phone', ''),
            "TEL;type=CELL:%s" % user.getProperty('cellphone', ''),
            "EMAIL:%s" % user.getProperty('email', ''),
            "TITLE:%s" % user.getProperty('jobtitle', ''),
            "NOTE:%s" % user.getProperty('description', ''),
        )
