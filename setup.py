from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.listusers',
      version=version,
      description="A search form for listing users.",
      long_description=open("README.rst").read() + "\n" +
          open(os.path.join("docs", "FUTURE.rst")).read() + "\n" +
          open(os.path.join("docs", "CREDITS.rst")).read() + "\n" +
          open(os.path.join("docs", "HISTORY.rst")).read() + "\n" +
          open(os.path.join("docs", "LICENSE.rst")).read(),
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
          'setuptools',
          'collective.js.datatables',
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
