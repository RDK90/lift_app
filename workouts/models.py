from django.db import models

# Create your models here.
class Training(models.Model):
    #Define data types
    date = models.DateField()
    exercise_category = models.CharField(max_length=10)
    exercise = models.CharField(max_length=80)
    set_number = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()
    rep_category = models.CharField(max_length=10)

    def __str__(self):
        return str(self.date)

class Exercises(models.Model):
    exercise = models.CharField(max_length=80)
    primary_exercise_body_part = models.CharField(max_length=20)
    secondary_exercise_body_part = models.CharField(max_length=20)

    def __str__(self):
        return str(self.exercise)