from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rute_api.algorithm import create_checkin
from rute_api.models import User, Route, DriveRequest
from rute_api.queries import get_drive_request_by_user
from rute_api.serializers import UserSerializer, RouteSerializer, DriveRequestSerializer


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

    def post(self, request, format=None, *args, **kwargs):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriveRequestView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        driver_uuid = self.kwargs['uuid']  # kwargs uuid is the driver user uuid
        drive_requests = get_drive_request_by_user(driver_uuid).values()
        return Response(drive_requests, status=status.HTTP_200_OK)

    def put(self, request, format=None, *args, **kwargs):
        drive_request_uuid = DriveRequest.objects.get(uuid=self.kwargs['uuid'])
        serializer = DriveRequestSerializer(drive_request_uuid, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_checkin(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None, *args, **kwargs):
        serializer = DriveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)