import xmltodict

from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.schema.availability import (
    GetBookableDaysResponse,
    GetBookableTimesResponse,
)


def get_bookable_days(
    agenda_id, appointment_type_id, start_date, end_date, resource_id=None
) -> GetBookableDaysResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "getBookableDays",
        AgendaId=agenda_id,
        AppointmentTypeId=appointment_type_id,
        StartDate=start_date,
        EndDate=end_date,
        ResourceId=resource_id,
    )
    json_resp = xmltodict.parse(resp.content)
    return GetBookableDaysResponse.parse_obj(json_resp["Response"])


def get_bookable_times(
    agenda_id,
    appointment_type_id,
    date,
    resource_id=None,
    start_time=None,
    end_time=None,
) -> GetBookableTimesResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "getBookableTimes",
        AgendaId=agenda_id,
        AppointmentTypeId=appointment_type_id,
        Date=date,
        ResourceId=resource_id,
        StartTime=start_time,
        EndTime=end_time,
    )
    json_resp = xmltodict.parse(resp.content)
    return GetBookableTimesResponse.parse_obj(json_resp["Response"])
