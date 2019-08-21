from django.urls import path

from . import views

app_name = "workouts"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('workouts/', views.get_all),
    path('workouts/<id>/', views.get_by_id),
]