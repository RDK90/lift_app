from django.urls import path
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import views
from . import workouts_api, characteristics_api, plans_api

app_name = "workouts"

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('workouts/', workouts_api.all_workouts, name='all_workouts'),
    path('plans/', plans_api.all_plans, name='all_plans'),
    path('workouts/<workout_id>/', workouts_api.workouts_by_id, name='id_workouts'),
    path('exercises/<exercise_name>/', views.exercises_by_name, name="name_exercises"),
    path('characteristics/<date>/', characteristics_api.characteristics_by_date, name="date_characteristics"),
    path('plans/<date>/', plans_api.plans_by_date, name="date_plans"),
    path('login', views.login, name="login"),
]
