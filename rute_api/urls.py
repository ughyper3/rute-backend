from django.urls import path
from .views import UserView, RouteView, DriveRequestView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('routes/', RouteView.as_view(), name='routes'),
    path('drive-requests/', DriveRequestView.as_view(), name='drive_requests_post'),
    path('drive-requests/<str:uuid>/', DriveRequestView.as_view(), name='drive_requests')
]