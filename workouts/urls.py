from django.urls import path

from .views import TrainingView

app_name = "workouts"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('workouts/', TrainingView.as_view()),
]