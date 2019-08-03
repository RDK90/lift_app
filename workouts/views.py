from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrainingSerializer
from rest_framework.decorators import api_view

from .models import Training

@api_view(['GET'])
def get_all(request):
    if request.method == "GET":
        workouts = Training.objects.all()
        training_serializer = TrainingSerializer(workouts, many=True)
        return Response({"workouts": training_serializer.data})

@api_view(['GET'])
def get_by_id(request, id):
    if request.method == "GET":
        workouts = Training.objects.filter(id=id).values()
        training_serializer = TrainingSerializer(workouts, many=True)
        return Response({"workouts": training_serializer.data})

