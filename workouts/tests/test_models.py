from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from workouts.models import Characteristics, Exercises, Plan, Training, Profile, TrainingVersionTwo, CharacteristicsVersionTwo, PlanVersionTwo


# Create your tests here.
class ModelsTest(TestCase):

    def test_training_str_method(self):
        training_date = Training(date='25/03/19')
        self.assertEqual(str(training_date), training_date.date)

    def test_exercise_str_method(self):
        exercise = Exercises(exercise="Bench Press")
        self.assertEqual(str(exercise), exercise.exercise)

    def test_characteristics_str_method(self):
        characteristics = Characteristics(date="25/03/19")
        self.assertEqual(str(characteristics), characteristics.date)

    def test_plan_str_method(self):
        plan = Plan(date="25/03/19")
        self.assertEqual(str(plan), plan.date)

    def test_profile_str_method(self):
        user = User.objects.create_user(
            username = 'test',
            password = 'test',
            email = 'test@test.com'
        )
        user.save()
        profile = Profile(user=user)
        self.assertEqual(str(profile), profile.user.username)
        User.objects.filter(username=user.username).delete()

    # v2 Tests
    def test_training_version_two_str_method(self):
        training_date = TrainingVersionTwo(date='25/03/19')
        self.assertEqual(str(training_date), training_date.date)

    def test_characteristics_version_two_str_method(self):
        characteristics = CharacteristicsVersionTwo(date="25/03/19")
        self.assertEqual(str(characteristics), characteristics.date)

    def test_plan_version_two_str_method(self):
        plan = PlanVersionTwo(date="25/03/19")
        self.assertEqual(str(plan), plan.date)