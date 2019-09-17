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

def format_date(workout_id):
    return "{}-{}-{}".format(workout_id[4:8], workout_id[2:4], workout_id[0:2])
        
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

@api_view(['GET', 'POST'])
def workouts_by_id(request, workout_id):
    date = format_date(workout_id)
    if request.method == "GET":
        if not validate_date(date):
            content = {"Error message": "Invalid date {} found. Correct date format is DDMMYYY".format(date)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        workouts = Training.objects.filter(date=date).values()
        if not workouts:
            content = {"Error message": "No workouts for date {} found".format(date)}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            training_serializer = TrainingSerializer(workouts, many=True)
            for workouts in training_serializer.data:
                workouts.pop("date")
            return Response({"date":date, "workout": training_serializer.data})
    if request.method == "POST":
        data = []
        date = format_date(request.data.get("date"))
        for post_data in request.data["workout"]:
            data.append({
                "date": date,
                "exercise_category": post_data.get("exercise_category"),
                "exercise": post_data.get("exercise"),
                "set_number": post_data.get("set_number"),
                "reps": post_data.get("reps"),
                "weight": post_data.get("weight"),
                "rep_category": post_data.get("rep_category")
            })
        training_serializer = TrainingSerializer(data=data, many=True)
        if training_serializer.is_valid():
            training_serializer.save()
            return Response(training_serializer.data, status=status.HTTP_201_CREATED)
        return Response(training_serializer.data, status=status.HTTP_400_BAD_REQUEST)


    

