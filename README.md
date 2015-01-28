[![Build Status](https://travis-ci.org/rockabox/django_warnings.svg?branch=master)](https://travis-ci.org/rockabox/django_warnings)
[![Coverage](http://img.shields.io/coveralls/rockabox/django_warnings/master.svg)](https://coveralls.io/r/rockabox/django_warnings?branch=master)

# django_warnings
A package that gives you dynamic warnings with your django models

## How-to use
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
    'Warning, 1 is not equal to 2'

Keep in mind that your model `warning_methods` will be called each time you use
the `warnings` property.
