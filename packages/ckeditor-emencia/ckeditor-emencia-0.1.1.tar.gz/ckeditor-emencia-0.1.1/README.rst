EmenciaCkeditor
===============

This library looks into in the ``INSTALLED_APPS`` for directories named
``editor-site-templates``  and explore their content to export a list of templates for
CKEditor.

Install
*******

You can retrieve it via pip: ::

    pip install django-datadownloader

Then add ``ckeditor_emencia`` in the ``INSTALLED_APPS`` and register the
``ckeditor_emencia.urls`` in the same prefix as ``ckeditor``.

Usage
*****

To create templates, drop an HTML file in a directory name ``editor-site-templates``
in an app: ::

    my_app/
        __init__.py
        models.py
        editor-site-templates/
            template1.html

To define title, description, or the image associated with the template, write
a file ``manifest.json`` at the root of the ``editor-site-templates/``
directory. This manifest is a JSON encoded dict. The key is the path relative
to ``editor-site-templates/`` and the value is a dict of keys title,
description and image. All the keys are optionnal. The image is relative to
``STATIC_URL``.

Sample resulting tree: ::

    my_app/
        __init__.py
        models.py
        static/
            template1-icon.png
        editor-site-templates/
            manifest.json
            template1.html

Sample ``manifest.json``: ::

    {
        "template1.html": {
            "title": "Template 1",
            "description": "description for template1",
            "image": "template1-icon.png",
        }
    }
