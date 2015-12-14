from django.core.urlresolvers import reverse
from django.test import override_settings, TestCase

from rest_framework import status

from django_warnings.models import Warning

from ..models import WarningsGeneratingModel


@override_settings(ROOT_URLCONF='django_warnings.urls')
class WarningsEndpointTest(TestCase):

    def test_empty_listing(self):
        """
        The listing endpoint response is valid for an empty set of Warnings
        """
        url = reverse('warning-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_non_empty_listing(self):
        """
        The listing endpoint response is valid for an non-empty set of Warnings
        """
        number_of_objects = 10
        for _ in xrange(number_of_objects):
            generating_object = WarningsGeneratingModel.objects.create()
            generating_object.generate_warnings()
        url = reverse('warning-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), number_of_objects)
        self.assertIn('id', response.data[0])
        self.assertIn('message', response.data[0])

    def test_no_duplicate_warnings(self):
        """
        We do not create duplicate warnings
        """
        generating_object = WarningsGeneratingModel.objects.create()
        generating_object.generate_warning('Im in a pickle')
        generating_object.generate_warning('Im in a pickle')

        self.assertTrue(generating_object.warnings.count(), 1)

    def test_detail(self):
        """
        The detail endpoint response is valid for a given Warning
        """
        generating_object = WarningsGeneratingModel.objects.create()
        generating_object.generate_warnings()
        warning_object = Warning.objects.all()[0]
        url = reverse('warning-detail', args=(warning_object.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], warning_object.id)
        self.assertEqual(response.data['message'], warning_object.message)

    def test_automatic_acknowledge(self):
        """
        The acknowledge endpoint, actually acknowledges a given Warning
        """
        generating_object = WarningsGeneratingModel.objects.create()
        generating_object.generate_warnings()
        warning_object = Warning.objects.all()[0]
        url = reverse('warning-acknowledge',
                      args=(warning_object.id,))

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], warning_object.id)
        self.assertEqual(response.data['message'], warning_object.message)

        # Refresh the `warning_object` and check it's acknowledged
        warning_object = Warning.objects.get(id=warning_object.id)
        self.assertIsNotNone(warning_object.last_acknowledged)
        self.assertIsNone(warning_object.last_acknowledger)
        self.assertTrue(warning_object.automatically_acknowledged)

    def test_non_automatic_acknowledge(self):
        """
        The acknowledge endpoint receives and stores the acknowledger
        """
        generating_object = WarningsGeneratingModel.objects.create()
        generating_object.generate_warnings()
        warning_object = Warning.objects.all()[0]
        url = reverse('warning-acknowledge',
                      args=(warning_object.id,))

        response = self.client.post(url, data={'user_id': 42})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], warning_object.id)
        self.assertEqual(response.data['message'], warning_object.message)

        # Refresh the `warning_object` and check it's acknowledged
        warning_object = Warning.objects.get(id=warning_object.id)
        self.assertIsNotNone(warning_object.last_acknowledged)
        self.assertEqual(warning_object.last_acknowledger, 42)
        self.assertFalse(warning_object.automatically_acknowledged)
