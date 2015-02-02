[![Build Status](https://travis-ci.org/rockabox/django_warnings.svg?branch=master)](https://travis-ci.org/rockabox/django_warnings)
[![Coverage](http://img.shields.io/coveralls/rockabox/django_warnings/master.svg)](https://coveralls.io/r/rockabox/django_warnings?branch=master)

# django_warnings
A package that gives you dynamic warnings with your django models

## How-to use
First of all, you need to `django_warnings` to your `INSTALLED_APPS`.

In order to generate Warnings from a Model, you need to add a Mixin to it and
to reference which methods will be used to actually produce Warnings.

    class TestModel(WarningsMixin, models.Model):

        name = models.TextField()

        warning_methods = ['some_warnings_method']

        # Used for easier assertion
        warning_message = 'Warning, 1 is not equal to 2'

        def some_warnings_method(self):
            warnings = []
            if 1 != 2:
                warnings.append(self.warning_message)
            return warnings

Then you can access a `warnings` property on every instance of your model.

    >> test_model = TestModel()
    >> test_model.warnings
    ['Warning, 1 is not equal to 2']

Keep in mind that your model `warning_methods` will be called each time you use
the `warnings` property.

## Django-rest-framework compatible API
You can access a REST API to the Warnings backend by just including a line into
your `urls.py`::

    urlpatterns = patterns(
        '',
        ...
        url(r'^warnings/',
            include('django_warnings.urls', namespace='warnings')),
        ...
    )

This will add an endpoint to acknowledge a Warning and to retrive information
from the Warnings stored in your database. You can do::

    GET  .../warnings/warning/                   Will return every stored Warning
    GET  .../warnings/warning/{id}               Will return an specific Warning
    POST .../warnings/warning/{id}/acknowledge   Will acknowledge a Warning

As part of the last POST call body you can specify a `user_id`, identifying the
user that is acknowledging the Warning.

The default behavior will be to return 'id' and 'message' for every Warnings
object. If you want to return different fields, you can extend the ViewSet::

    from django_warnings.views import WarningViewSet

    class MyWarningViewSet(WarningViewSet):
        serializer_fields = ('message', 'last_generated')
