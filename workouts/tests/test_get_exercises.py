import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Training
from workouts.serializers import TrainingSerializer

# initialize the APIClient app
client = Client()

class GetExercisesTest(TestCase):

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

        def test_get_exercise_by_name(self):
            response = client.get(reverse('exercises:name_exercises'), kwargs={'ExerciseName':'Low Bar Squat'})
            exercise_data = Training.objects.filter(exercise="Low Bar Squat").values()
            serializer = TrainingSerializer(exercise_data, many=True)
            self.assertEqual(response.data['exercise'], serializer.data[0]['exercise'])
            self.assertEqual(response.status_code, status.HTTP_200_OK)