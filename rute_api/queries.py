from rute_api.models import DriveRequest


def get_drive_request_by_user(driver_uuid):
    drive_requests = DriveRequest.objects.filter(
        route__car__owner_id=driver_uuid,
        deleted=False,
        is_canceled=False,
        is_accepted=None
    ).values()
    return drive_requests

