#!/usr/bin/env python

import os
import sys
from django.conf import settings

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


# for Django 1.7
import django
try:
    django.setup()
except AttributeError:
    pass


from flake8.engine import get_style_guide
from flake8.main import DEFAULT_CONFIG, print_report
from django_nose.runner import NoseTestSuiteRunner

flake8_style = get_style_guide(parse_argv=True, config_file=DEFAULT_CONFIG)
report = flake8_style.check_files()
if report.total_errors > 0:
    print_report(report, flake8_style)
    sys.exit(1)

test_runner = NoseTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['tests'])
if failures > 0:
    sys.exit(1)
