from django.db import models

from django_warnings.decorators import register_warning
from django_warnings.warnings import DjangoWarning
from django_warnings.mixins import WarningsMixin


class WarningsGeneratingModel(WarningsMixin, models.Model):
    """
    A Model for testing the warnings system
    """
    name = models.TextField()

    # Used for easier assertion
    warning_message = 'Warning, 1 is not equal to 2'

    @register_warning
    def some_warning_method(self):
        """
        A method that raises a DjangoWarning if a warning situation is found
        """
        if 1 != 2:
            raise DjangoWarning(
                self.warning_message, identifier='123', url_params={
                    'arbitrary_param': 'arbitrary_value'
                }
            )
