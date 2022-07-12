from rute_api.models import DriveRequest
from django.db.models.query import QuerySet


def get_drive_request_by_user(driver_uuid: str) -> QuerySet:
    drive_requests = DriveRequest.objects.filter(
        route__car__owner_id=driver_uuid,
        deleted=False,
        is_canceled=False,
        is_accepted=None
    )
    return drive_requests

