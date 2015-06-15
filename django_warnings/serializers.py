import ast

from rest_framework import serializers

from .models import Warning


class WarningsField(serializers.ReadOnlyField):
    """
    This will be the Field normally imported outside the library

    It uses WarningModelSerializer internally to generate the final response
    """

    read_only = True
    required = False

    def __init__(self, *args, **kwargs):
        # Desired fields are kept and will be passed to WarningModelSerializer
        self.warning_fields = kwargs.pop('fields', [])

        # On the `to_native` method, we want to receive the parent object
        # instead of just the `warnings` field
        kwargs['source'] = '*'

        super(WarningsField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        super(WarningsField, self).to_representation(obj)

        if hasattr(obj, 'generate_warnings'):
            obj.generate_warnings()

        return WarningModelSerializer(
            obj.warnings.all(), many=True, fields=self.warning_fields).data


class WarningModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer for the Warning model

    It allows to specify which fields to use at the point of initializing it
    """

    class Meta:
        model = Warning
        fields = ('id', 'content_type', 'object_id', 'subject', 'message',
                  'first_generated', 'last_generated', 'identifier',
                  'url_params', 'acknowledged', 'last_acknowledger',
                  'last_acknowledged')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])

        super(WarningModelSerializer, self).__init__(*args, **kwargs)

        # Drop any fields that are not specified in the `fields` argument.
        # Copied from an example on DRF documentation.
        allowed = set(fields)
        existing = set(self.fields.keys())

        for field_name in existing - allowed:
            self.fields.pop(field_name)

    def to_representation(self, obj):
        """
        Convert url_params into native data type, as its been stringified
        """
        data = super(WarningModelSerializer, self).to_representation(obj)
        if 'url_params' in data:
            data['url_params'] = ast.literal_eval(data['url_params'])

        return data
