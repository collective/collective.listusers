from collective.listusers.config import MEMBER_PROPERTIES_TO_EXCLUDE
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope.component import getUtility
from zope.interface import implements
from zope.schema import getFieldNames
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory


class UserAttributesVocabulary(object):
    """Vocabulary factory for user attributes."""
    implements(IVocabularyFactory)

    def __call__(self, context):
        schema_provider = getUtility(IUserDataSchemaProvider)
        schema = schema_provider.getSchema()
        user_attributes = getFieldNames(schema)

        items = [SimpleTerm(attr, attr, attr) for attr in user_attributes
                 if attr not in MEMBER_PROPERTIES_TO_EXCLUDE]

        return SimpleVocabulary(items)

UserAttributesVocabularyFactory = UserAttributesVocabulary()
