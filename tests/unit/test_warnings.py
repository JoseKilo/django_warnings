from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from django_warnings.models import Warning
from ..models import WarningsGeneratingModel


class WarningsMixinTest(TestCase):

    def test_warnings_property_contains_warnings(self):
        """
        Make a model generate a Warning and check the result
        """
        warning_object = WarningsGeneratingModel.objects.create()

        self.assertTrue(hasattr(warning_object, 'warnings'))
        self.assertTrue(
            warning_object.warning_message in warning_object.warnings
        )

    def test_warnings_are_stored_into_database(self):
        """
        Instantiate a model reporting warnings, it generates a Warning object
        """
        warning_object = WarningsGeneratingModel.objects.create()

        warnings = warning_object.warnings
        stored_warning = Warning.objects.all()[0]

        self.assertEqual(len(warnings), 1)
        self.assertEqual(Warning.objects.count(), 1)
        self.assertEqual(stored_warning.message, warnings[0])

    def test_stored_warning_contains_subject(self):
        """
        Any stored Warning references the class and method that generated it
        """
        warning_object = WarningsGeneratingModel.objects.create()

        warning_object.warnings
        warning = Warning.objects.all()[0]

        self.assertEqual(Warning.objects.count(), 1)
        self.assertEqual(warning.subject, 'tests.models.some_warnings_method')

    def test_stored_warning_contains_first_and_last_generated_dates(self):
        """
        Any stored Warning references its first and last occurrence
        """
        warning_object = WarningsGeneratingModel.objects.create()

        warning_object.warnings
        warning = Warning.objects.all()[0]

        self.assertEqual(Warning.objects.count(), 1)
        self.assertIsNotNone(warning.first_generated)
        self.assertEqual(warning.last_generated - warning.first_generated,
                         timedelta())

    def test_repeated_warnings_ocurrences(self):
        """
        New occurrences increase the `last_generated` field
        """
        warning_object = WarningsGeneratingModel.objects.create()

        before = timezone.now()
        warning_object.warnings
        warning_object.warnings
        after = timezone.now()
        warning = Warning.objects.all()[0]

        self.assertEqual(Warning.objects.count(), 1)
        self.assertIsNotNone(warning.first_generated)
        self.assertTrue(timedelta() <
                        warning.last_generated - warning.first_generated <
                        after - before)

    def test_stored_warning_references_the_object_that_generated_it(self):
        """
        Any stored Warning allows to retrieve the original object causing it
        """
        warning_object = WarningsGeneratingModel.objects.create()

        warning_object.warnings
        warning = Warning.objects.all()[0]
        original_object = warning.content_object

        self.assertEqual(Warning.objects.count(), 1)
        self.assertEqual(original_object, warning_object)

    def test_stored_warning_is_unacknowledged_by_default(self):
        """
        Any stored Warning is not acknowledged when first generated
        """
        warning_object = WarningsGeneratingModel.objects.create()

        warning_object.warnings
        warning = Warning.objects.all()[0]

        self.assertEqual(Warning.objects.count(), 1)
        self.assertFalse(warning.acknowledged)
        self.assertIsNone(warning.automatically_acknowledged)
        self.assertIsNone(warning.last_acknowledger)
        self.assertIsNone(warning.last_acknowledged)

    def test_acknowledge_warning(self):
        """
        A Warning can be acknowledged, then it gets related fields filled
        """
        user_id = 3
        warning_object = WarningsGeneratingModel.objects.create()
        warning_object.warnings
        warning = Warning.objects.all()[0]

        warning.acknowledge(user_id)

        self.assertEqual(Warning.objects.count(), 1)
        self.assertTrue(warning.acknowledged)
        self.assertFalse(warning.automatically_acknowledged)
        self.assertEqual(warning.last_acknowledger, user_id)
        self.assertIsNotNone(warning.last_acknowledged)

    def test_automatically_acknowledge_warning(self):
        """
        A Warning is acknowledged automatically by not specifying a `user_id`
        """
        warning_object = WarningsGeneratingModel.objects.create()
        warning_object.warnings
        warning = Warning.objects.all()[0]

        warning.acknowledge()

        self.assertEqual(Warning.objects.count(), 1)
        self.assertTrue(warning.acknowledged)
        self.assertTrue(warning.automatically_acknowledged)
        self.assertIsNone(warning.last_acknowledger)
        self.assertIsNotNone(warning.last_acknowledged)
