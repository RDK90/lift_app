from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from workouts.api_support import *

from .models import Characteristics, Plan, Training
from .serializers import (CharacteristicsSerializer, PlanSerializer,
                          TrainingSerializer)

@api_view(['GET', 'PUT'])
def exercises_by_name(request, exercise_name):
    """
    Method:
    Get exercise data per exercise

    Endpoint:
    GET /exercises/<exercise_name>/
    """

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

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)
