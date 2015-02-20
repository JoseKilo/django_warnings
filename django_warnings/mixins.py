from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Q, F

from .models import Warning


class WarningsMixin(object):
    """
    A Mixin to add warning methods/properties to models

    The model you mixin in to should decorate warning methods with the
    `register_warning` decorator, to generate the warning, simple return your
    warning message from the method, or an iterable of emssages for multiple
    warnings
    """

    def generate_warning(self, message, method=None, identifier=None,
                         url_params=None):
        """
        Given a message and an optional error_code, generate a warning
        """
        params = {
            'message': message,
            'content_type': ContentType.objects.get_for_model(self),
            'object_id': self.id,
        }

        if method:
            params.update({'subject': method})

        if identifier:
            params.update({'identifier': identifier})

        if url_params:
            params.update({'url_params': url_params})

        warning, created = Warning.objects.update_or_create(
            defaults={'last_generated': timezone.now()}, **params
        )

        return warning

    def generate_warnings(self):
        """
        This method will be called by the serialiser field, it picks up any
        methods defined in your models warning_methods and calls them
        """
        for method in self.__class__.__dict__:
            if hasattr(getattr(self.__class__, method), 'is_warning'):
                getattr(self, method)()

    @property
    def warnings(self):
        """
        Return all warnings associated with this model that have not yet been
        acknowledged, or have been generated again since acknowledgement
        """
        return Warning.objects.filter(
            Q(content_type=ContentType.objects.get_for_model(self)),
            Q(object_id=self.id),
            Q(last_acknowledged=None) |
            Q(last_acknowledged__lt=F('last_generated')),
        )
