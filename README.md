reguser
=======

Simple, clean and modern reusable app for Django user registration


Overview
--------

This app differs from the popular django-registration package in the following ways:

  * actively maintained and supports the latest version of Django;
  * uses cryptographic signing instead of storing Registration Profiles in the database;
  * comes with useful basic templates!
  * is cleaner, simpler and easier to work with. 


Requirements
------------

  * Python 2.7
  * Django 1.7
  * shortuuid
  * django-bootstrap-form (if you're going to use the included templates)


Installation
------------

    pip install -r -e git+git@github.com:a115/reguser.git#egg=reguser

Then include 'reguser' in your INSTALLED_APPS. 


Usage and customization
-----------------------

The simplest way to use the app is to hook it up to an endpoint in your urls.py, like this:
    
    url(r'^accounts/', include('reguser.urls')),

Then run your server and hit `/accounts/register/`
