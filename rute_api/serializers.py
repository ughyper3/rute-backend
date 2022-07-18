from rest_framework import serializers
from rute_api.models import User, Route, DriveRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class DriveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveRequest
        fields = '__all__'
