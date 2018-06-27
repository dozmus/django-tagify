django-tagify
----------------

A django tag input field using Tagify_ built for Django 2.0.

.. _Tagify: https://github.com/yairEO/tagify/

Usage
===============

1. Models: Use ``TagsField`` to represent a tags field.
2. Forms: Make sure you display ``form.media`` in the html template, for the widget to render correctly.
3. Widget settings: Pass the settings dictionary as follows ``TagsField(widget_settings={...}``.

 * You can specify if 'duplicates' are allowed (boolean).
 * You can specify 'autocomplete' (boolean) - this matches from the whitelist.
 * You can specify 'enforceWhitelist' (boolean).
 * You can specify 'maxTags' (int).
 * You can specify the 'whitelist' (list containing strings).
 * You can specify the 'blacklist' (list containing strings).
 * You can specify the 'delimiters' (string).
 * You can specify the RegEx 'pattern' to validate the input (string).

Note: The results of these settings are not automatically verified in the Python code.

Installation
===============

1. Install the module

  .. code-block::

      pip install django-tagify

2. Add ``django_tagify`` to your ``INSTALLED_APPS`` setting in the Django ``settings.py``.

    Example:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...other installed apps
            'django_tagify',
        )
