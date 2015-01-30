from django.db import models

from django_warnings.mixins import WarningsMixin


class WarningsGeneratingModel(WarningsMixin, models.Model):
    """
    A Model for testing the warnings system
    """
    name = models.TextField()

    warning_methods = ['some_warnings_method']

    # Used for easier assertion
    warning_message = 'Warning, 1 is not equal to 2'

    def some_warnings_method(self):
        warnings = []
        if 1 != 2:
            warnings.append(self.warning_message)
        return warnings
