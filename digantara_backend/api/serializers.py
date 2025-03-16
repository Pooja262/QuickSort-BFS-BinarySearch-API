from rest_framework import serializers
from .models import AlgorithmLog

class AlgorithmLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgorithmLog
        fields = '__all__'
