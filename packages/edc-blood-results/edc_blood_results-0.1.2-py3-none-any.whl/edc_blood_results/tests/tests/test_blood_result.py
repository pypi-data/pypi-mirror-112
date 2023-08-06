from django.test import TestCase

from edc_blood_results_app.models import BloodResultsFbc, SubjectVisit


class TestBloodResult(TestCase):
    def test_ok(self):
        subject_visit = SubjectVisit.objects.create()
        BloodResultsFbc.objects.create()
