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
        self.user = Profile.objects.create(user=test_user)
        self.client = APIClient()
        self.client.force_authenticate(user=test_user)

        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=8, weight=30, rep_category="Warm up"
        )
        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=8, weight=40, rep_category="Warm up"
        )
        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=8, weight=50, rep_category="Work"
        )

        self.valid_payload = {
            "date" : "16092019",
            "workout": [
                {
                    "exercise_category":"T1",
                    "exercise": "Deadlift",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 70,
                    "rep_category": "Warm up"
                },
                {
                    "exercise_category":"T1",
                    "exercise": "Deadlift",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 110,
                    "rep_category": "Warm up"
                }
            ]
        }
        self.invalid_payload = {
            "date" : "999",
            "workout": [
                {
                    "exercise_category":"T1",
                    "exercise": "Deadlift",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 70,
                    "rep_category": "Warm up"
                },
                {
                    "exercise_category":"T1",
                    "exercise": "Deadlift",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 110,
                    "rep_category": "Warm up"
                }
            ]
        }

    def test_get_all_workouts_version_two(self):
        response = self.client.get(reverse('workouts:all_workouts_v2'))
        workout_data = TrainingVersionTwo.objects.all()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.data[0]['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workouts_by_date_version_two(self):
        response = self.client.get(reverse('workouts:workouts_by_date_v2', kwargs={'date':'25032019'}))
        workout_data = TrainingVersionTwo.objects.filter(user=self.user, date="2019-03-25").values()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.data['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workouts_by_invalid_date_version_two(self):
        response = self.client.get(reverse('workouts:workouts_by_date_v2', kwargs={'date': '22092019'}))
        workout_data = TrainingVersionTwo.objects.filter(user=self.user, date="2019-09-22").values()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_workouts_by_invalid_datetype_version_two(self):
        response = self.client.get(reverse('workouts:workouts_by_date_v2', kwargs={'date': '999'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_workouts_no_auth_token_version_two(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.get(reverse('workouts:workouts_by_date_v2', kwargs={'date':'25032019'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_workout_by_date_version_two(self):
        response = self.client.post(
            reverse("workouts:workouts_by_date_v2", kwargs={'date': self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_datetype_workout_by_date_version_two(self):
        response = self.client.post(
            reverse("workouts:workouts_by_date_v2", kwargs={'date': self.invalid_payload["date"]}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_workouts_no_auth_token_version_two(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.post(
            reverse("workouts:workouts_by_date_v2", kwargs={'date': self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_workout_by_date_version_two(self):
        response = self.client.put(
            reverse("workouts:workouts_by_date_v2", kwargs={"date": self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_invalid_datetype_workout_by_date_version_two(self):
        response = self.client.put(
            reverse("workouts:workouts_by_date_v2", kwargs={"date": self.invalid_payload["date"]}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_workouts_no_auth_token_date_version_two(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.put(
            reverse("workouts:workouts_by_date_v2", kwargs={"date": self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_workouts_by_date_version_two(self):
        response = self.client.delete(
            reverse("workouts:workouts_by_date_v2", kwargs={"date": self.valid_payload["date"]})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_workouts_by_invalid_date_version_two(self):
        response = self.client.delete(
            reverse("workouts:workouts_by_date_v2", kwargs={"date": "999"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_workous_no_auth_token_version_two(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.delete(
            reverse("workouts:workouts_by_date_v2", kwargs={"date": self.valid_payload["date"]})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        User.objects.filter(username="nerd").delete()
        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        ).delete()
        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=8, weight=30, rep_category="Warm up"
        ).delete()
        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=8, weight=40, rep_category="Warm up"
        ).delete()
        TrainingVersionTwo.objects.create(
            user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=8, weight=50, rep_category="Work"
        ).delete()