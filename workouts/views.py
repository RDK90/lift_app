from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrainingSerializer

from .models import Training

class TrainingView(APIView):
    def get(self, request):
        workouts = Training.objects.all()
        training_serializer = TrainingSerializer(workouts, many=True)
        return Response({"workouts": training_serializer.data})

