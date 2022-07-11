from django.contrib import admin
from rute_api.models import User, Car, Route, CheckIn, DriveRequest


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "rating",
        "is_active"
    ]


class CarAdmin(admin.ModelAdmin):
    list_display = [
        "maker",
        "color",
        "license_plate"
    ]


class RouteAdmin(admin.ModelAdmin):
    list_display = [
        "car",
        "starting_location",
        "end_location",
        "starting_time",
        "available_seats",
        "contribution"
    ]


class CheckInAdmin(admin.ModelAdmin):
    list_display = [
        "checkin_time",
        "route",
        "user"
    ]


class DriveRequestAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "route",
        "is_accepted",
        "is_canceled"
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(DriveRequest, DriveRequestAdmin)