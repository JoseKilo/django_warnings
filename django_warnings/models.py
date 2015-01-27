from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class Warning(models.Model):
    """
    Warnings are persistent notifications of issues requiring attention

    They are connected to one or more of campaigns, line items, ad units,
    creatives.
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    subject = models.TextField()
    message = models.TextField()

    first_generated = models.DateTimeField()
    last_generated = models.DateTimeField()

    acknowledged = models.BooleanField(default=False)
    # Soft-FK to accounts.User
    last_acknowledger = models.PositiveIntegerField(null=True, default=None)
    last_acknowledged = models.DateTimeField(null=True, default=None)

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
