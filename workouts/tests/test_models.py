from django.test import TestCase
from workouts.models import Training
from datetime import datetime
# Create your tests here.
class ModelsTest(TestCase):

    def test_str_method(self):
        training_date = Training(date='25/03/19')
        self.assertEqual(str(training_date), training_date.date)

