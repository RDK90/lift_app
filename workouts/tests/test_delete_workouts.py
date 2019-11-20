import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Training
from workouts.serializers import TrainingSerializer
import pytest

# initialize the APIClient app
client = Client()

class DeleteWorkoutsTest(TestCase):

    def setUp(self):
        Training.objects.create(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        Training.objects.create(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=21, reps=8, weight=40, rep_category="Warm up"
        )
        Training.objects.create(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=8, weight=60, rep_category="Warm up"
        )
        Training.objects.create(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=8, weight=80, rep_category="Warm up"
        )
        

    def test_delete_workouts_by_id(self):
        response = client.delete(
            reverse("workouts:id_workouts", kwargs={"workout_id": "16092019"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_date_workouts_by_id(self):
        response = client.delete(
            reverse("workouts:id_workouts", kwargs={"workout_id": "999"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
