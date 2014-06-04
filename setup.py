import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'reguser',
    version = '0.0.1a1',
    packages = find_packages(),
    include_package_data = True,
#    setup_requires = [ "setuptools-git >= 1.0", ],
    license = 'GNU LESSER GENERAL PUBLIC LICENSE Version 3',
    description = 'Simple, clean and modern reusable app for Django user registration.',
    long_description = README,
    url = 'https://github.com/a115/reguser',
    author = 'Jordan Dimov / A115',
    author_email = 'jdimov@a115.co.uk',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
