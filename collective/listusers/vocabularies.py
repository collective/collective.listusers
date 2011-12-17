from plone.app.users.userdataschema import IUserDataSchema
from zope.schema.vocabulary import SimpleVocabulary


def get_user_attributes_vocabulary():
    attributes = IUserDataSchema.names()
    terms = []

    for attribute in attributes:
        terms.append(
            SimpleVocabulary.createTerm(attribute, attribute, attribute),)

    return SimpleVocabulary(terms)

user_attributes_vocabulary = get_user_attributes_vocabulary()
