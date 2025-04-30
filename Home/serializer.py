from rest_framework import serializers
from .models import Clint, Doctor

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clint
        fields = ['email', 'password']


