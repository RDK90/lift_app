from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

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

#v2 Training Model
class TrainingVersionTwo(models.Model):
    user = models.ForeignKey(Profile, default=1, on_delete=models.CASCADE)
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

class Characteristics(models.Model):
    date = models.DateField()
    week = models.IntegerField()
    time = models.TimeField()
    toughness = models.IntegerField()
    awakeness = models.IntegerField()
    anxiety = models.IntegerField()
    soreness = models.IntegerField()
    enthusiasm = models.IntegerField()

    def __str__(self):
        return str(self.date)

#v2 Characteristics Model
class CharacteristicsVersionTwo(models.Model):
    user = models.ForeignKey(Profile, default=1, on_delete=models.CASCADE)
    date = models.DateField()
    week = models.IntegerField()
    time = models.TimeField()
    toughness = models.IntegerField()
    awakeness = models.IntegerField()
    anxiety = models.IntegerField()
    soreness = models.IntegerField()
    enthusiasm = models.IntegerField()

    def __str__(self):
        return str(self.date)
        
class Plan(models.Model):
    date = models.DateField()
    exercise_category = models.CharField(max_length=10)
    exercise = models.CharField(max_length=80)
    set_number = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()
    rep_category = models.CharField(max_length=10)

    def __str__(self):
        return str(self.date)

# v2 Plan 
class PlanVersionTwo(models.Model):
    user = models.ForeignKey(Profile, default=1, on_delete=models.CASCADE)
    date = models.DateField()
    exercise_category = models.CharField(max_length=10)
    exercise = models.CharField(max_length=80)
    set_number = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()
    rep_category = models.CharField(max_length=10)

    def __str__(self):
        return str(self.date)