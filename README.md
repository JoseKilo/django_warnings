[![Build Status](https://travis-ci.org/rockabox/django_warnings.svg?branch=master)](https://travis-ci.org/rockabox/django_warnings)
[![Coverage](http://img.shields.io/coveralls/rockabox/django_warnings/master.svg)](https://coveralls.io/r/rockabox/django_warnings?branch=master)

# django_warnings
A package that gives you dynamic warnings with your django models

## How-to use
First of all, you need to `django_warnings` to your `INSTALLED_APPS`.

In order to generate Warnings from a Model, you need to add a Mixin to it and
to decorate the methods that will be used to actually produce Warnings.

    from django_warnings.mixins import WarningsMixin
    from django_warnings.decorators import register_warning


    class TestModel(WarningsMixin, models.Model):

        name = models.TextField()

        @register_warning
        def some_multi_warning_method(self):
            warnings = []

            if 1 != 2:
                warnings.append('Warning 1 is not equal to 2')

            if 2 != 3:
                warnings.append('Warning 2 is not equal to 3')

            return warnings

        @register_warning
        def some_multi_warning_method(self):
            warnings = []
            if 1 != 2:
                return 'Warning 1 is not equal to 2'

Then you can access a `warnings` property on every instance of your model.

    >> test_model = TestModel()
    >> test_model.warnings.all()
    ['Warning, 1 is not equal to 2']

Keep in mind that your models warning methods will be called each time you use
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

## Consuming warnings on the frontend (optional)

In your settings.py set the possible warning codes

    WARNING_CODES = (
        ('SOMECODE', 'Some Code Label',)
    )

when you make an warning . i.e-

    instance = Model()
    instance.generate_warning('Something weird here', identifier='SOMECODE', url_params={
        'object_id': 234,
        'arbitrary_param': 'arbitrary_value'
    }])

Then when you receive the warning back from the API, it will look something like*:

    {
        'id': 1,
        'message': 'Something weird is going on',
        'identifier': 'SOMECODE',
        'url_params': {
            'object_id': 234,
            'arbitrary_param': 'arbitrary_value'
        }
    }

    Then your frontend could construct a resolution message, such as:

    error_resolutions = {
        'SOMECODE': '{arbitrary_param} is not a valid thing, go to http://yourapp.com/{object_id} to fix it'
    }

    Using the identifier and url params to help construct this message

* subject to having defined these parameters in the `fields` attribute mentioned above

## Also worth noting:
The default ordering of warnings is by `last_generated`
