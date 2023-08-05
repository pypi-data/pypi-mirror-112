# -*- coding: utf-8 -*-

from ckeditor_emencia.views import EditorTemplatesListView
from django.conf.urls import url

urlpatterns = [
    url(r'^editor_site_templates.js$',
        EditorTemplatesListView.as_view(),
        name='ckeditor-editor-site-templates'),
]
