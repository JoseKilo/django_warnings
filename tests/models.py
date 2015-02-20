from django.db import models

from django_warnings.mixins import WarningsMixin
from django_warnings.decorators import register_warning


class WarningsGeneratingModel(WarningsMixin, models.Model):
    """
    A Model for testing the warnings system, with a warning method that
    returns a single warning
    """
    name = models.TextField()

    # Used for easier assertion
    warning_message = 'Warning, 1 is not equal to 2'

    @register_warning
    def some_single_warning_method(self):
        """
        A method that returns an error message, or nothing
        """
        if 1 != 2:
            return self.warning_message


class MultiWarningsGeneratingModel(WarningsMixin, models.Model):
    """
    A Model for testing the warnings system, with a warning method that
    returns multiple warnings
    """

    name = models.TextField()

    warning_message_1 = 'Warning, 1 is not equal to 2'
    warning_message_2 = 'Warning, 2 is not equal to 3'

    @register_warning
    def some_multi_warnings_method(self):
        """
        A method that returns an iterable of error messages, or nothing
        """
        warnings = []

        if 1 != 2:
            warnings.append(self.warning_message_1)

        if 2 != 3:
            warnings.append(self.warning_message_2)

        return warnings
