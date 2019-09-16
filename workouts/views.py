from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrainingSerializer
from rest_framework.decorators import api_view
from datetime import datetime
from rest_framework import status

from .models import Training

def validate_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False
        
@api_view(['GET'])
def get_all(request):
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

@api_view(['GET'])
def get_by_id(request, workout_id):
    date = "{}-{}-{}".format(workout_id[4:8], workout_id[2:4], workout_id[0:2])
    if not validate_date(date):
        content = {"Error message": "Invalid date {} found. Correct date format is DDMMYYY".format(date)}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    workouts = Training.objects.filter(date=date).values()
    if not workouts:
        content = {"Error message": "No workouts for date {} found".format(date)}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == "GET":
            training_serializer = TrainingSerializer(workouts, many=True)
            for workouts in training_serializer.data:
                workouts.pop("date")
            return Response({"date":date, "workout": training_serializer.data})

    

