from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Warning


class WarningsMixin(object):
    """
    A Mixin to add a `warnings` property to models

    The model should have a class level property called `warning_methods` that
    contains names of the methods that are to be called. Every one of these
    methods should return a list of warning messages
    """

    warning_methods = []

    @property
    def warnings(self):
        """
        The model property that contains the aggregated warnings
        """
        warnings = []
        for method in self.warning_methods:
            callable_method = getattr(self, method)
            outcome = callable_method()

            for message in outcome:
                warning, _ = Warning.objects.update_or_create(
                    subject='{}.{}'.format(self.__class__.__module__, method),
                    message=message,
                    content_type=ContentType.objects.get_for_model(self),
                    object_id=self.id,
                    defaults={
                        'last_generated': timezone.now()
                    }
                )

                if (warning.last_acknowledged is None or
                        warning.last_acknowledged < warning.last_generated):
                    warnings.append(message)

        return warnings
