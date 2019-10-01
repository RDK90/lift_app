from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrainingSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from workouts.api_support import *
from .models import Training

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
        if not validate_date(date):
            content = {"Error message": "Invalid date {} found. Correct date format is DDMMYYY".format(date)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
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
        workouts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

