from django.contrib import admin
from rute_api.models import User, Car, Route, CheckIn


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


admin.site.register(User, UserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(CheckIn, CheckInAdmin)