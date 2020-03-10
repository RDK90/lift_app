from django.urls import path

from . import views

app_name = "workouts"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('workouts/', views.all_workouts, name='all_workouts'),
    path('plans/', views.all_plans, name='all_plans'),
    path('workouts/<workout_id>/', views.workouts_by_id, name='id_workouts'),
    path('exercises/<exercise_name>/', views.exercises_by_name, name="name_exercises"),
    path('characteristics/<date>/', views.characteristics_by_date, name="date_characteristics"),
    path('plans/<date>/', views.plans_by_date, name="date_plans"),
    path('login', views.login),
]