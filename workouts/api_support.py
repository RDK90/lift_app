from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

from .serializers import CharacteristicsSerializer, TrainingSerializer


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

def format_exercise_data(request):
    if "workout" in request.data and "exercise" in request.data:
        data = []
        exercise = request.data.get("exercise")
        for post_data in request.data["workout"]:
            data.append({
                "date": format_date(post_data.get("date")),
                "exercise_category": post_data.get("exercise_category"),
                "exercise": exercise,
                "set_number": post_data.get("set_number"),
                "reps": post_data.get("reps"),
                "weight": post_data.get("weight"),
                "rep_category": post_data.get("rep_category")
            })
        return data
    else:
        return False

def format_characteristics_data(request):
    request.data['date'] = format_date(request.data.get('date'))
    return [request.data]

def put_post_workouts_by_id_response(request):
    data = format_data(request)
    training_serializer = TrainingSerializer(data=data, many=True)
    if training_serializer.is_valid():
        training_serializer.save()
        return Response(training_serializer.data, status=status.HTTP_201_CREATED)
    return Response(training_serializer.data, status=status.HTTP_400_BAD_REQUEST)

def put_post_exercises_by_name_response(request):
    data = format_exercise_data(request)
    if data != False:
        training_serializer = TrainingSerializer(data=data, many=True)
        if training_serializer.is_valid():
            training_serializer.save()
            return Response(training_serializer.data, status=status.HTTP_201_CREATED)
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

def put_post_characteristics_by_date_response(request):
    data = format_characteristics_data(request)
    characteristics_serializer = CharacteristicsSerializer(data=data, many=True)
    if characteristics_serializer.is_valid():
        characteristics_serializer.save()
        return Response(characteristics_serializer.data, status=status.HTTP_201_CREATED)
    else:
        content = {"Error Message": "Data is not valid"}
        return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
