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
        return Response(training_serializer.data)

@api_view(['GET'])
def get_by_id(request, workout_id):
    year = workout_id[4:8]
    month = workout_id[2:4]
    day = workout_id[0:2]
    date = "{}-{}-{}".format(year, month, day)
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
            response_data = {"date":date, "workout": training_serializer.data}
            return Response(response_data)

    

