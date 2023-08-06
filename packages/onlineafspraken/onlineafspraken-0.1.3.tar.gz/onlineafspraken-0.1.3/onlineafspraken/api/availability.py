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
        agendaId=agenda_id,
        appointmentTypeId=appointment_type_id,
        resourceId=resource_id,
        startDate=start_date,
        endDate=end_date,
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
        agendaId=agenda_id,
        appointmentTypeId=appointment_type_id,
        date=date,
        resourceId=resource_id,
        startTime=start_time,
        endTime=end_time,
    )
    json_resp = xmltodict.parse(resp.content)
    return GetBookableTimesResponse.parse_obj(json_resp["Response"])
