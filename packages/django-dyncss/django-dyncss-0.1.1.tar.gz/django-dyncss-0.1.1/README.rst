=============
django-dyncss
=============

`Django DynCSS <https://github.com/jcolot/django-dyncss>`_ is an extension
to `Django <https://github.com/django/django>`_ which adds the possibility
to store css files in the Django DB with simple versioning.

Installation
============

Install the latest version from pypi.python.org:

    pip install django-dyncss

Install the development version by cloning the source from github.com:

    pip install git+https://github.com/jcolot/django-dyncss.git

Configuration
=============

Add the package to your `INSTALLED_APPS`:
::

    INSTALLED_APPS = (
        ...
        'dyncss',
    )

Add the url path in your main urls.py.
::

    urlpatterns = [
        ...
        path('dyncss/', include('dyncss.urls')),
    ]

Usage
=====

Create a CSS File from the Django Admin

Add a link to that file in your Django template
::

    <link rel="stylesheet" href="dyncss/example.css">

You can also use the template tag
::

    {% load dyncss %}

    {% dyncss 'example.css' inline=True %}

The parameter `inline` when `True` allows to render the file inline within `<style>` tags

License
=======

-   Released under MIT License
-   Copyright (c) 2021 Julien Colot <julien.colot@gmail.com>

Resources
=========

-   `Code <https://github.com/jcolot/django-dyncss>`_
