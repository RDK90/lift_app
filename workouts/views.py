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

@api_view(['GET'])
def all_plans(request):
    if request.method == "GET":
        workouts = Plan.objects.all()
        plan_serializer = PlanSerializer(workouts, many=True)
        response_data = [{"date":"", "workout":[]}]
        index = 0
        for plan in plan_serializer.data:
            date = plan.pop("date")
            if response_data[index]["date"] == "" or response_data[index]["date"] != date:
                response_data.append({"date":date, "workout":[plan]})
                index = index + 1
            else:
                response_data[index]["workout"].append(plan)
        response_data.pop(0)
        return Response(response_data)

@api_view(['GET','PUT', 'POST', 'DELETE'])
def plans_by_date(request, date):
    date = format_date(date)
    try:
        workouts = Plan.objects.filter(date=date).values()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        if not workouts:
            content = {"Error message": "No plan for date {} found".format(date)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            plan_serializer = PlanSerializer(workouts, many=True)
            for plans in plan_serializer.data:
                plans.pop("date")
            return Response({"date":date, "plan": plan_serializer.data})
    if request.method == "PUT" or request.method == "POST":
        return put_post_workouts_by_id_response(request)
    if request.method == "DELETE":
        plan = Plan.objects.filter(date=date)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
