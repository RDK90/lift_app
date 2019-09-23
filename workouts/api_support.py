from datetime import datetime
from rest_framework.response import Response
from .serializers import TrainingSerializer
from rest_framework import status

def validate_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False

def format_date(workout_id):
    return "{}-{}-{}".format(workout_id[4:8], workout_id[2:4], workout_id[0:2])

def format_data(request):
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
    return data

def put_post_workouts_by_id_response(request):
    data = format_data(request)
    training_serializer = TrainingSerializer(data=data, many=True)
    if training_serializer.is_valid():
        training_serializer.save()
        return Response(training_serializer.data, status=status.HTTP_201_CREATED)
    return Response(training_serializer.data, status=status.HTTP_400_BAD_REQUEST)