import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Training
from workouts.serializers import TrainingSerializer

# initialize the APIClient app
client = Client()

class GetWorkoutsTest(TestCase):

    def setUp(self):
        Training.objects.create(
            id=2, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        Training.objects.create(
            id=3, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=4, weight=70, rep_category="Work"
        )
        Training.objects.create(
            id=4, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=4, weight=110, rep_category="Work"
        )
        Training.objects.create(
            id=5, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=4, weight=120, rep_category="Work"
        )

    def test_get_all_workouts(self):
        response = client.get(reverse('workouts:all_workouts'))
        workout_data = Training.objects.all()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_workouts_by_id(self):
        response = client.get(reverse('workouts:id_workouts', kwargs={'workout_id':'25032019'}))
        workout_data = Training.objects.filter(date="2019-03-25").values()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.data['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_workouts_by_id(self):
        response = client.get(reverse('workouts:id_workouts', kwargs={'workout_id':'22032019'}))
        workout_data = Training.objects.filter(date="2019-03-22").values()
        serializer = TrainingSerializer(workout_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_invalid_datetype_workouts_by_id(self):
        response = client.get(reverse('workouts:id_workouts', kwargs={'workout_id':'999'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)