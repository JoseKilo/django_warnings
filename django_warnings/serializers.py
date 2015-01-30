from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Warning


class WarningSerializer(serializers.Serializer):
    """
    This will be the Serializer normally imported outside the library

    It uses WarningModelSerializer internally to generate the final response
    """

    def __init__(self, *args, **kwargs):

        # Desired fields are kept and will be pass to WarningModelSerializer
        self.warning_fields = kwargs.pop('fields', [])

        # On the `to_native` method, we want to receive the parent object
        # instead of just the `warnings` field
        kwargs['source'] = '*'
        kwargs['read_only'] = True

        super(WarningSerializer, self).__init__(*args, **kwargs)

    def to_native(self, obj):

        # Trigger the Warnings generation
        obj.warnings

        # Fetch generated Warnings
        warnings = Warning.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        )
        return WarningModelSerializer(
            warnings, many=True, fields=self.warning_fields).data


class WarningModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer for the Warning model

    It allows to specify which fields to use at the point of initializing it
    """

    class Meta:
        model = Warning
        fields = ('id', 'content_type', 'object_id', 'subject', 'message',
                  'first_generated', 'last_generated',
                  'acknowledged', 'last_acknowledger', 'last_acknowledged')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])

        super(WarningModelSerializer, self).__init__(*args, **kwargs)

        # Drop any fields that are not specified in the `fields` argument.
        # Copied from an example on DRF documentation.
        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)
