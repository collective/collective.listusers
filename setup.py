import os
from setuptools import setup, find_packages


setup(name='collective.listusers',
      version='1.3',
      description="A search form for listing users.",
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='plone search users group LDAP',
      author='NiteoWeb Ltd.',
      author_email='info@niteoweb.com',
      url='https://github.com/collective/collective.listusers',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.elephantvocabulary',
          'collective.js.datatables',
          'plone.app.z3cform',
          'plone.app.vocabularies',
          'setuptools',
          'pas.plugins.ldap',
          'zope.schema>=3.8.0',  # required to use IContextAwareDefaultFactory
      ],
      extras_require={
          'test': [
              'mock',
              'plone.app.testing',
           ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
