from rest_framework import serializers
from.models import  LogUpload
from .models import ForwarderData

class ForwarderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForwarderData
        fields = '__all__'

class LogUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogUpload
        fields = '__all__'

