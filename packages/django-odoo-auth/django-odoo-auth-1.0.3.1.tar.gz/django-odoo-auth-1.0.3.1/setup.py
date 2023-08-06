from os import path

from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-odoo-auth',
    version='1.0.3.1',
    packages=['odoo_auth', 'odoo_auth.migrations'],
    license='Apache-2.0 License',
    description='Custom django auth backend for authorization via odoo',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/w0rng/django-odoo-auth',
    author='w0rng, Julien DRECQ',
    install_requires=[
        'django',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
