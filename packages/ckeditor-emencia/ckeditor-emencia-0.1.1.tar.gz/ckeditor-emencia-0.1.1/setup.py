# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='ckeditor-emencia',
    version=__import__('ckeditor_emencia').__version__,
    description=__import__('ckeditor_emencia').__doc__,
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    author='Grégoire ROCHER',
    author_email='support@emencia.com',
    url='https://github.com/emencia/ckeditor-emencia',
    license='GNU Affero General Public License v3',
    packages=find_packages(
        exclude=[
            'tests',
            'tests.*',
        ]
    ),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        "django>=1.8",
        "django-ckeditor>=5.0",
    ],
    extras_require={
        'dev': [
            'flake8',
            'pytest',
            'pytest-django',
            'pytest-pythonpath',
            'twine',
        ]
    },
    include_package_data=True,
    zip_safe=False
)
