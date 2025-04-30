from rest_framework import serializers
from Home.models import *

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['password','name', 'age', 'specialization', 'education', 'about','experence','specialization','rating']


class DoctorProfileSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='User.name', read_only=True)
    class Meta:
        model = Room
        fields = '__all__'
        extra_fields = ['doctor_name']

class ChatSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class BookSerilizer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='User.name', read_only=True)
    class Meta:
        model = BookDoctor
        fields = '__all__'
        extra_fields = ['user_name']