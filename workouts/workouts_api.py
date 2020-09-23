from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from workouts.api_support import *

from .models import Training, TrainingVersionTwo, Profile
from .serializers import TrainingSerializer


@api_view(['GET'])
def all_workouts(request):
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

@api_view(['GET'])
def get_all_workouts_version_two(request):
    if request.method == "GET":
        profile_user = Profile.objects.get(user=request.user)
        workouts = TrainingVersionTwo.objects.filter(user=profile_user)
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
def get_workouts_by_date_version_two(request, date):
    formatted_date = format_date(date)
    try:
        profile_user = Profile.objects.get(user=request.user)
        workouts = TrainingVersionTwo.objects.filter(user=profile_user, date=formatted_date).values()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        if not workouts:
            content = {"Error message": "No workouts for date {} found".format(formatted_date)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            training_serializer = TrainingSerializer(workouts, many=True)
            for workouts in training_serializer.data:
                workouts.pop("date")
            return Response({"date":formatted_date, "workout": training_serializer.data})
    if request.method == "POST" or request.method == "PUT":
        return put_post_workouts_by_id_response(request)
    if request.method == "DELETE":
        workouts = Training.objects.filter(date=formatted_date)
        workouts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)