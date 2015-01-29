from django.test import TestCase

from rest_framework import serializers

from django_warnings.serializers import WarningSerializer
from ..models import WarningsGeneratingModel


class WarningsGeneratingSerializer(serializers.ModelSerializer):

    warnings = WarningSerializer(fields=('id', 'message'))

    class Meta:
        model = WarningsGeneratingModel
        fields = ('name', 'warnings',)


class WarningsSerializerTest(TestCase):

    def test_serializer_returns_warnings(self):
        """
        Serialize a model with Warnings associated to it
        """
        warning_model = WarningsGeneratingModel.objects.create()
        data = WarningsGeneratingSerializer(warning_model).data

        self.assertEqual(data['warnings'][0]['message'],
                         warning_model.warning_message)

    def test_serialize_queryset_returns_warnings(self):
        """
        Serialize a queryset of models with Warnings associated to them
        """
        number_of_instances = 10
        for _ in xrange(number_of_instances):
            WarningsGeneratingModel.objects.create()

        warning_models = WarningsGeneratingModel.objects.all()
        data = WarningsGeneratingSerializer(warning_models, many=True).data

        self.assertEqual(len(data), number_of_instances)
        for element in data:
            self.assertEqual(element['warnings'][0]['message'],
                             WarningsGeneratingModel.warning_message)

    def test_serializer_can_contain_subject(self):
        """
        Use a serializer returning the `subject` the Warning object
        """
        class SubjectSerializer(serializers.ModelSerializer):
            warnings = WarningSerializer(fields=('subject',))

            class Meta:
                model = WarningsGeneratingModel
                fields = ('name', 'warnings',)

        warning_model = WarningsGeneratingModel.objects.create()
        data = SubjectSerializer(warning_model).data
        warnings = data['warnings']

        self.assertEqual(len(warnings), 1)
        self.assertListEqual(warnings[0].keys(), ['subject'])
        self.assertEqual(warnings[0]['subject'],
                         'tests.models.some_warnings_method')

    def test_serializer_can_contain_every_field(self):
        """
        Use a serializer returning the every field on the Warning object
        """
        all_fields = ('id', 'content_type', 'object_id', 'subject', 'message',
                      'first_generated', 'last_generated',
                      'acknowledged', 'last_acknowledger', 'last_acknowledged')

        class FullSerializer(serializers.ModelSerializer):
            warnings = WarningSerializer(fields=all_fields)

            class Meta:
                model = WarningsGeneratingModel
                fields = ('name', 'warnings',)

        warning_model = WarningsGeneratingModel.objects.create()
        data = FullSerializer(warning_model).data
        warnings = data['warnings']

        self.assertEqual(len(warnings), 1)
        self.assertEqual(set(warnings[0].keys()), set(all_fields))
        self.assertEqual(warnings[0]['object_id'], warning_model.id)
