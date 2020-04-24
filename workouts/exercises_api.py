from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from workouts.api_support import *

from .models import Training
from .serializers import TrainingSerializer


@api_view(['GET', 'PUT'])
def exercises_by_name(request, exercise_name):

    workouts = Training.objects.filter(exercise=exercise_name).values()
    training_serializer = TrainingSerializer(workouts, many=True)
    if len(training_serializer.data) == 0:
        content = {"Error Message: Exercise {} not found".format(exercise_name)}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        for workouts in training_serializer.data:
            workouts.pop("exercise")
        return Response({"exercise": exercise_name, "workout":training_serializer.data})
    if request.method == "PUT":
        return put_post_exercises_by_name_response(request)
