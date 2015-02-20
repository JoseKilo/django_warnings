#!/usr/bin/env python

import os
import sys

import django
from django.conf import settings

from tests import runtests


DIRNAME = os.path.dirname(__file__)
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'TEST_NAME': ':memory:',  # this is the default, NAME is not used
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {'isolation_level': None}
        },
        'redshift': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    DEBUG=True,
    MIDDLEWARE_CLASSES=[],
    INSTALLED_APPS=(
        'django.contrib.contenttypes',

        'django_warnings',
        'tests'
    ),
    LANGUAGE_CODE='en-gb',
    ROOT_URLCONF='urls',
)


if __name__ == '__main__':
    try:
        # for Django 1.7
        django.setup()
    except AttributeError:
        pass

    failures = runtests.flake8()
    if failures > 0:
        sys.exit(1)

    failures = runtests.nose()
    if failures > 0:
        sys.exit(1)
