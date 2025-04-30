from rest_framework import serializers
from Home.models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clint
        fields = ['password','name', 'age', 'gender', 'api_key', 'address']


class UserProfileSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Clint
        fields = '__all__'

class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    class Meta:
        model = Room
        fields = '__all__'
        extra_fields = ['doctor_name']


class ChatSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class BookSerilizer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    class Meta:
        model = BookDoctor
        fields = '__all__'
        extra_fields = ['doctor_name']