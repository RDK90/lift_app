import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from workouts.models import Training
from workouts.serializers import TrainingSerializer


class TestWorkouts(TestCase):

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        Training.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        Training.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=4, weight=70, rep_category="Work"
        )
        Training.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=4, weight=110, rep_category="Work"
        )
        Training.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=4, weight=120, rep_category="Work"
        )

        self.valid_training = Training.objects.create(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        self.invalid_training = Training.objects.create(
            date="2019-09-23", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
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

    def test_get_all_workouts(self):
        response = self.client.get(reverse('workouts:all_workouts'))
        workout_data = Training.objects.all()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.data[0]['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_workouts_by_id(self):
        response = self.client.get(reverse('workouts:id_workouts', kwargs={'workout_id':'25032019'}))
        workout_data = Training.objects.filter(date="2019-03-25").values()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.data['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_workouts_by_id(self):
        response = self.client.get(reverse('workouts:id_workouts', kwargs={'workout_id':'22032019'}))
        workout_data = Training.objects.filter(date="2019-03-22").values()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_invalid_datetype_workouts_by_id(self):
        response = self.client.get(reverse('workouts:id_workouts', kwargs={'workout_id':'999'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_workouts_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.get(reverse('workouts:id_workouts', kwargs={'workout_id':'25032019'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_post_workout_by_id(self):
        response = self.client.post(
            reverse("workouts:id_workouts", kwargs={'workout_id': self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_datetype_workout_by_id(self):
        response = self.client.post(
            reverse("workouts:id_workouts", kwargs={'workout_id': self.invalid_payload["date"]}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_workouts_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.post(
            reverse("workouts:id_workouts", kwargs={'workout_id': self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_workout_by_id(self):
        response = self.client.put(
            reverse("workouts:id_workouts", kwargs={"workout_id": self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_invalid_datetype_workout_by_id(self):
        response = self.client.put(
            reverse("workouts:id_workouts", kwargs={"workout_id": self.invalid_payload["date"]}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_workouts_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.put(
            reverse("workouts:id_workouts", kwargs={"workout_id": self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_workouts_by_id(self):
        response = self.client.delete(
            reverse("workouts:id_workouts", kwargs={"workout_id": "16092019"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_date_workouts_by_id(self):
        response = self.client.delete(
            reverse("workouts:id_workouts", kwargs={"workout_id": "999"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_workouts_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.delete(
            reverse("workouts:id_workouts", kwargs={"workout_id": "16092019"})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def tearDown(self):
        User.objects.filter(username="nerd").delete()
        Training.objects.filter(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        ).delete()
        Training.objects.filter(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=4, weight=70, rep_category="Work"
        ).delete()
        Training.objects.filter(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=4, weight=110, rep_category="Work"
        ).delete()
        Training.objects.filter(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=4, weight=120, rep_category="Work"
        ).delete()
        Training.objects.filter(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        ).delete()
        Training.objects.filter(
            date="2019-09-23", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        ).delete()
