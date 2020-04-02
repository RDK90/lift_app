from datetime import datetime

from django.test import TestCase

from workouts.models import Characteristics, Exercises, Plan, Training


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
