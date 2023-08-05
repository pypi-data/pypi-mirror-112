# -*- coding: utf-8 -*-

import os
import json
import logging
import collections

from django.apps import apps
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)

CKEditorTemplate = collections.namedtuple('CKEditorTemplate', ['title', 'description', 'image', 'html'])


class TemplateList(object):
    """
    Recursively list all HTML file in settings.CKEDITOR_EDITOR_TEMPLATES_PATH
    that didn't start with "_" and

    On the root of the settings.CKEDITOR_EDITOR_TEMPLATES_PATH directory,
    should resides a "manifest.json" file that contain a map to your content templates to
    declare their optionnal title and description. When a content template has no
    declared title it take his relative path as title, and the default description is
    "No description".

    Your "manifest.json" file should look like :

        {
            "foo.html": {
                "title": "Dummy",
                "image": "grid_row.gif",
                "description": "Dummy template for testing"
            }
        }

    The template HTML is taken from the template filename given at the key name.

    Take care to make valid JSON, else this will raise exception. Also note that content
    templates are indexed on their relative path.
    """

    def __iter__(self):
        return iter(self.get_templates())

    def get_templates(self):
        # Perform scanning on all known templates directory
        site_templates = {}
        for app in reversed(list(apps.get_app_configs())):
            site_templates.update(self._get_templates_from_root(os.path.join(app.path, 'editor-site-templates')))
        return list(site_templates.values())

    def _get_templates_from_root(self, root):
        try:
            with open(os.path.join(root, 'manifest.json'), 'r') as manifest_file:
                manifest = json.load(manifest_file)
        except IOError as ioe:
            if ioe.errno != 2:  # ENOENT
                raise
            manifest = {}
        except Exception:
            logger.error('When reading %s', os.path.join(root, 'manifest.json'))
            raise

        for _root, _dirs, files in os.walk(root):
            for name in files:
                if name.startswith('_') or not name.endswith('.html'):
                    continue

                absolute = os.path.join(root, name)
                relative = os.path.relpath(absolute, root)
                if relative in manifest:
                    meta = manifest[relative]
                else:
                    meta = {}

                with open(absolute, 'r') as fp:
                    template_data = CKEditorTemplate(
                        meta.get('title') or name,
                        meta.get('description', ''),
                        meta.get('image', ''),
                        fp.read()
                    )

                # If the entry is defined in the manifest
                yield name, template_data


class CachedTemplateList(TemplateList):
    def __iter__(self):
        return iter(self.cached_templates)

    @cached_property
    def cached_property(self):
        return list(super(CachedTemplateList, self).get_templates())
