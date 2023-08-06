#!/usr/bin/env python

from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='flask-docusign',
      version='0.1.0',
      description='Simple DocuSign client for Flask',
      url='https://github.com/adyachok/adocusign',
      author='Andras Gyacsok',
      author_email='atti.dyachok@gmail.com',
      license='MIT',
      packages=['flask_docusign'],
      install_requires=[
          'certifi==2021.5.30',
          'cffi==1.14.6',
          'chardet==4.0.0',
          'click==8.0.1',
          'cryptography==3.4.7',
          'docusign-esign==3.10.0',
          'fastapi-camelcase==1.0.2',
          'Flask==2.0.1',
          'idna==2.10',
          'itsdangerous==2.0.1',
          'Jinja2==3.0.1',
          'MarkupSafe==2.0.1',
          'nose==1.3.7',
          'pycparser==2.20',
          'pydantic==1.8.2',
          'pydantic[email]',
          'pyhumps==3.0.2',
          'PyJWT==1.7.1',
          'python-dateutil==2.8.1',
          'requests==2.25.1',
          'six==1.16.0',
          'typing-extensions==3.10.0.0',
          'urllib3==1.26.6',
          'Werkzeug==2.0.1',
      ],
      long_description_content_type='text/markdown',
      long_description=long_description,
      zip_safe=False)
