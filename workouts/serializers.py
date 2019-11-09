from .models import Training, Characteristics
from rest_framework import serializers

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

class CharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = '__all__'