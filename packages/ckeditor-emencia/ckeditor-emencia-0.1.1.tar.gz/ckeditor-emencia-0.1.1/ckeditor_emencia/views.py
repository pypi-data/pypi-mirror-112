# -*- coding: utf-8 -*-
"""
Views to customize CKEditor

These views are for admin staff only, we don't want to expose them.
"""
import json

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from django.template import Template, Context

from ckeditor_emencia.models import TemplateList


class EditorTemplatesListView(View):
    """
    Return the list in a Javascript file :

        // Register a templates definition set named "default".
        CKEDITOR.addTemplates( 'default', {
            // The name of sub folder which hold the shortcut preview images of the
            // templates.
            imagesPath: '/static/ckeditor/editor-site-templates/',

            // The templates definitions.
            templates: [
                {
                    title: 'Grid row',
                    image: 'grid_row.gif',
                    description: 'Sample',
                    html: '<div class="row"></div>'
                }
            ]
        }

    """

    template = Template(
        u'''CKEDITOR.addTemplates('default', {
    imagesPath: '{{imagespath}}',
    templates: {{json_list|safe}}
});'''
    )
    template_list = TemplateList()

    def dispatch(self, request, *args, **kw):
        return super(EditorTemplatesListView, self).dispatch(request, *args, **kw)

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            self.template.render(Context({
                'imagespath': settings.STATIC_URL,
                'json_list': json.dumps(self.get_template_list())
            })),
            content_type='application/javascript'
        )

    def get_template_list(self):
        return [t._asdict() for t in self.template_list]
