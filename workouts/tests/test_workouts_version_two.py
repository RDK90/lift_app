import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from workouts.models import TrainingVersionTwo, Profile
from workouts.serializers import TrainingSerializer

class TestWorkoutsVersionTwo(TestCase):

    def setUp(self):
        test_user = User.objects.create(username="nerd")
        user = Profile.objects.create(user=test_user)
        self.client = APIClient()
        self.client.force_authenticate(user=test_user)

        TrainingVersionTwo.objects.create(
            user=user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        TrainingVersionTwo.objects.create(
            user=user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=8, weight=30, rep_category="Warm up"
        )
        TrainingVersionTwo.objects.create(
            user=user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=8, weight=40, rep_category="Warm up"
        )
        TrainingVersionTwo.objects.create(
            user=user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=8, weight=50, rep_category="Work"
        )

    def test_get_all_workouts_version_two(self):
        response = self.client.get(reverse('workouts:all_workouts_v2'))
        workout_data = TrainingVersionTwo.objects.all()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.data[0]['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        User.objects.filter(username="nerd").delete()