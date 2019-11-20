from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrainingSerializer, CharacteristicsSerializer, PlanSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from workouts.api_support import *
from .models import Training, Characteristics, Plan

@api_view(['GET'])
def all_workouts(request):
    """
    Method:
    Get all workouts

    Endpoint:
    GET /workouts
    """
    if request.method == "GET":
        workouts = Training.objects.all()
        training_serializer = TrainingSerializer(workouts, many=True)
        response_data = [{"date":"", "workout":[]}]
        index = 0
        for workout in training_serializer.data:
            date = workout.pop("date")
            if response_data[index]["date"] == "" or response_data[index]["date"] != date:
                response_data.append({"date":date, "workout":[workout]})
                index = index + 1
            else:
                response_data[index]["workout"].append(workout)
        response_data.pop(0)
        return Response(response_data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def workouts_by_id(request, workout_id):
    date = format_date(workout_id)
    try:
        workouts = Training.objects.filter(date=date).values()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        if not workouts:
            content = {"Error message": "No workouts for date {} found".format(date)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            training_serializer = TrainingSerializer(workouts, many=True)
            for workouts in training_serializer.data:
                workouts.pop("date")
            return Response({"date":date, "workout": training_serializer.data})
    if request.method == "POST" or request.method == "PUT":
        return put_post_workouts_by_id_response(request)
    if request.method == "DELETE":
        workouts = Training.objects.filter(date=date)
        workouts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def characteristics_by_date(request, date):
    date = format_date(date)
    try:
        characteristics = Characteristics.objects.filter(date=date).values()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        if not characteristics:
            content = {"Error Message: Characteristics for date {} not found".format(date)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            characteristics_serializer = CharacteristicsSerializer(characteristics, many=True)
            return Response(characteristics_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST' or request.method == 'PUT':
        return put_post_characteristics_by_date_response(request)
    elif request.method == 'DELETE':
        characteristics = Characteristics.objects.filter(date=date)
        characteristics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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