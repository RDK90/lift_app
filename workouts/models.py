from django.db import models

# Create your models here.
class Workout(models.Model):
    #Define choices
    REP_CAT = ((WARMUP:'Warm up'), (WORK:'Work'), (AMRAP:'Amrap'))

    #Define data types
    date = models.DateField()
    exercise_category = models.CharField(max_length=10)
    exercise = models.CharField(max_length=80)
    set_number = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()
    rep_category = models.CharField(max_length=10, choices=REP_CAT)
