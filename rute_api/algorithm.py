from rute_api.models import CheckIn, Route, User
from rute_api.serializers import RouteSerializer


def create_checkin(serializer: RouteSerializer):
    if serializer.data['is_accepted']:
        route = Route.objects.get(uuid=serializer.data['route'])
        starting_time = route.starting_time
        user = User.objects.get(uuid=serializer.data['user'])
        checkin = CheckIn.objects.create(checkin_time=starting_time, route=route, user=user)
        checkin.save()

