from rest_framework import serializers
from.models import  LogUpload
from .models import ForwarderData, User, APIKey
#due to erroor of object
# from rest_meets_djongo.serializers import DjongoModelSerializer    

class ForwarderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForwarderData
        fields = '__all__'

class LogUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogUpload
        fields = '__all__'


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__' 



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name','role', 'email', 'password']

        #how to hide the password
        extra_kwargs = {

            'password': {'write_only': True}
        }

    #hash password     django default
    def create(self, validated_data):  
        password =  validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)      ##validated data without extract password
        if password is not None:
            instance.set_password(password)        ##this function provided by django.
        instance.save()
        return instance    

     