from rest_framework import viewsets
from .serializers import TrainingSerializer
from .models import Training

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
