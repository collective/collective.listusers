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
        items = [SimpleTerm(ua, ua, ua) for ua in user_attributes]

        return SimpleVocabulary(items)

UserAttributesVocabularyFactory = UserAttributesVocabulary()
