from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rute_api.models import User, Route
from rute_api.queries import get_drive_request_by_user
from rute_api.serializers import UserSerializer, RouteSerializer


class UserView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True).data
        return Response(serialized_users, status=status.HTTP_200_OK)


class RouteView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        routes = Route.objects.all()
        serialized_routes = RouteSerializer(routes, many=True).data
        response = serialized_routes
        return Response(response, status=status.HTTP_200_OK)


class DriveRequestView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        driver_uuid = self.kwargs['driver_uuid']
        drive_requests = get_drive_request_by_user(driver_uuid).values()
        return Response(drive_requests, status=status.HTTP_200_OK)