"""VCard view."""

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

VCARD_TEMPLATE = """BEGIN:VCARD
FN:%s
N:%s
ORG:%s
ADR:%s;%s
TEL;type=WORK:%s
TEL;type=CELL:%s
EMAIL:%s
TITLE:%s
NOTE:%s
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

        vcard = VCARD_TEMPLATE % (
            user.getProperty('fullname', ''),
            user.getProperty('fullname', ''),
            user.getProperty('organization', ''),
            user.getProperty('location', ''),
            user.getProperty('location', ''),
            user.getProperty('phone', ''),
            user.getProperty('cellphone', ''),
            user.getProperty('email', ''),
            user.getProperty('jobtitle', ''),
            user.getProperty('description', ''),
        )

        self.request.response.setHeader('Content-Type', 'text/x-vcard')
        self.request.response.setHeader(
            "Content-disposition", "attachment;filename=%s.vcf" % user.getId()
        )

        return vcard
