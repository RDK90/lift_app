import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from workouts.models import Plan
from workouts.serializers import PlanSerializer


class TestPlans(TestCase):

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        Plan.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        Plan.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=4, weight=70, rep_category="Work"
        )
        Plan.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=4, weight=110, rep_category="Work"
        )
        Plan.objects.create(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=4, weight=120, rep_category="Work"
        )

        self.valid_plan = Plan.objects.create(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )

        self.invalid_plan = Plan.objects.create(
            date="2019-09-23", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )

        self.valid_payload = {
            "date": "16092019",
            "workout": [
                {
                    "exercise_category": "T1",
                    "exercise": "Squat",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 60,
                    "rep_category": "Warm up"
                },
                {
                    "exercise_category": "T1",
                    "exercise": "Squat",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 90,
                    "rep_category": "Warm up"
                }
            ]
        }

        self.invalid_payload = {
            "date": "999",
            "workout": [
                {
                    "exercise_category": "T1",
                    "exercise": "Squat",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 60,
                    "rep_category": "Warm up"
                },
                {
                    "exercise_category": "T1",
                    "exercise": "Squat",
                    "set_number": 1,
                    "reps": 4,
                    "weight": 90,
                    "rep_category": "Warm up"
                }
            ]
        }

    def test_get_all_plans(self):
        response = self.client.get(reverse('workouts:all_plans'))
        plan_data = Plan.objects.all()
        serializer = PlanSerializer(plan_data, many=True)
        self.assertEqual(response.data[0]['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_plan_by_date(self):
        response = self.client.get(reverse('workouts:date_plans', kwargs={'date':'25032019'}))
        plan_data = Plan.objects.filter(date='2019-03-25').values()
        serializer = PlanSerializer(plan_data, many=True)
        self.assertEqual(response.data['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_plan_by_id(self):
        response = self.client.get(reverse('workouts:date_plans', kwargs={'date':'22032019'}))
        plan_data = Plan.objects.filter(date="2019-03-22").values()
        serializer = PlanSerializer(plan_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_invalid_datetype_plan_by_id(self):
        response = self.client.get(reverse('workouts:date_plans', kwargs={'date':'999'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_plans_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.get(reverse('workouts:all_plans'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_plan_by_date(self):
        response = self.client.delete(
            reverse("workouts:date_plans", kwargs={"date":"25032019"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_plan_by_invalid_date(self):
        response = self.client.delete(
            reverse("workouts:date_plans", kwargs={"date":"999"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_plans_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.delete(
            reverse("workouts:date_plans", kwargs={"date":"25032019"})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_plan_by_date(self):
        response = self.client.post(
            reverse("workouts:date_plans", kwargs={"date":"16092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_plan_by_invalid_date(self):
        response = self.client.post(
            reverse("workouts:date_plans", kwargs={"date":"999"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_plan_by_invalid_payload(self):
        response = self.client.post(
            reverse("workouts:date_plans", kwargs={"date":"16092019"}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_plan_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.post(
            reverse("workouts:date_plans", kwargs={"date":"16092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_plan_by_date(self):
        response = self.client.put(
            reverse("workouts:date_plans", kwargs={"date":"16092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_plan_by_invalid_date(self):
        response = self.client.put(
            reverse("workouts:date_plans", kwargs={"date":"999"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_plan_by_invalid_payload(self):
        response = self.client.put(
            reverse("workouts:date_plans", kwargs={"date":"23092019"}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_plan_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.put(
            reverse("workouts:date_plans", kwargs={"date":"16092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        User.objects.filter(username="nerd").delete()
        Plan.objects.filter(
             date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        ).delete()            
        Plan.objects.filter(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=4, weight=70, rep_category="Work"
        ).delete()
        Plan.objects.filter(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=4, weight=110, rep_category="Work"
        ).delete()
        Plan.objects.filter(
            date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=4, weight=120, rep_category="Work"
        ).delete()
        Plan.objects.filter(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        ).delete()
        Plan.objects.filter(
            date="2019-09-23", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        ).delete()
