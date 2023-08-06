# coding=utf-8
"""
viledayacloud

py setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
"""

from setuptools import setup

setup(name='viledayacloud',
      version='1.0.2',
      packages=['viledayacloud'],
      url='https://www.vileda-professional.com/',
      license='Creative Commons Attribution 4.0 International',
      author='FHCS GmbH',
      author_email='support@fhcs.zendesk.com',
      description='Classes and functions to use in software integration with Yandex Cloud services',
      install_requires=['aiohttp>=3.7.4.post0'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Other Environment',
                   'License :: Other/Proprietary License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Topic :: Utilities'],
      zip_safe=False,
      python_requires='>=3.8'
      )
