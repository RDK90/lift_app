from workouts import views
from django.test import TestCase
from workouts.models import Training
import json
from rest_framework.test import APIRequestFactory
from unittest.mock import patch

class WorkoutAPITest(TestCase):  
    def setUp(self):
        self.factory = APIRequestFactory()
        self.workout_data = ""
        with open("workouts/tests/workout_sample.json", "r") as json_file:
            self.workout_data = json.load(json_file)

    def test_all_workouts(self):
        with patch("requests.get") as mock_call_get:
            mock_call_get.return_value.content = self.workout_data
            request = self.factory.get('/workouts')
            response = views.get_all(request)
            self.assertEqual(response.status_code, 200)

    def test_single_workout(self):
        with patch("requests.get") as mock_call_get:
            mock_call_get.return_value.content = self.workout_data
            request = self.factory.get('/workouts/2')
            response = views.get_by_id(request, 2)
            self.assertEqual(response.status_code, 200)
