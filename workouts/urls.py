from django.urls import path

from . import views

app_name = "workouts"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('workouts/', views.get_all, name='all_workouts'),
    path('workouts/<workout_id>/', views.get_by_id, name='id_workouts'),
]