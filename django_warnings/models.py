from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from jsonfield import JSONField


class Warning(models.Model):
    """
    Warnings are persistent notifications of issues requiring attention.

    They are connected to one or more of instances of one or more models.
    They contain a `subject` referencing the model and method that generated
    them, as well as timestamps of the first and last generation time.

    Warnings can also be acknowledged by a user or an automatic process. We
    keep an id of the user that caused the Warning to be registered (if any)
    and the last timestamp when that happened.
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    identifier = models.TextField(blank=True, null=True)
    url_params = JSONField(
        help_text='An object with keys that help the frontend form a url',
        blank=True, null=True
    )

    subject = models.TextField()
    message = models.TextField()

    first_generated = models.DateTimeField()
    last_generated = models.DateTimeField()

    acknowledged = models.BooleanField(default=False)
    # Soft-FK to a model representing the User that acknowledges the Warning
    last_acknowledger = models.PositiveIntegerField(null=True, default=None)
    last_acknowledged = models.DateTimeField(null=True, default=None)

    class Meta:
        ordering = ('last_generated',)

    def __str__(self):
        return self.subject

    @property
    def automatically_acknowledged(self):
        """
        Determine whether or not the Warning was acknowledged by a user
        """
        if self.last_acknowledged is None:
            return None
        return self.last_acknowledger is None

    def acknowledge(self, user_id=None):
        """
        Mark this stored Warning as acknowledged
        """
        self.acknowledged = True
        self.last_acknowledger = user_id
        self.last_acknowledged = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        """
        Instead of using `auto_now_add=True` we add `first_generated` here to
        avoid it to be generated after `last_generated`.
        """
        if self.pk is None:
            self.first_generated = self.last_generated
        super(Warning, self).save(*args, **kwargs)
