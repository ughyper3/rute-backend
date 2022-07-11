from django.urls import path
from .views import UserView, RouteView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('routes/', RouteView.as_view(), name='routes')
]