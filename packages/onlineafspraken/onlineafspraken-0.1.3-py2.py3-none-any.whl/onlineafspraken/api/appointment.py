import xmltodict

from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.schema.appointment import (
    CancelAppointmentResponse,
    ConfirmAppointmentResponse,
    GetAppointmentsResponse,
    GetAppointmentResponse,
    SetAppointmentResponse,
)


def cancel_appointment(
    appointment_id, mode=None, remarks=None, confirmation=None, dry_run=None
) -> CancelAppointmentResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "cancelAppointment",
        id=appointment_id,
        mode=mode,
        remarks=remarks,
        confirmation=confirmation,
        dryRun=dry_run,
    )
    json_resp = xmltodict.parse(resp.content)
    return CancelAppointmentResponse.parse_obj(json_resp["Response"])


def confirm_appointment(
    appointment_id, confirmation_code
) -> ConfirmAppointmentResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "confirmAppointment", id=appointment_id, confirmationCode=confirmation_code
    )
    json_resp = xmltodict.parse(resp.content)
    return ConfirmAppointmentResponse.parse_obj(json_resp["Response"])


def get_appointments(
    agenda_id,
    start_date,
    end_date,
    customer_id=None,
    appointment_type_id=None,
    resource_id=None,
    include_cancelled=None,
    limit=None,
    offset=None,
) -> GetAppointmentsResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "getAppointments",
        agendaId=agenda_id,
        startDate=start_date,
        endDate=end_date,
        customerId=customer_id,
        appointmentTypeId=appointment_type_id,
        resourceId=resource_id,
        includeCancelled=include_cancelled,
        limit=limit,
        offset=offset,
    )
    json_resp = xmltodict.parse(resp.content)
    return GetAppointmentsResponse.parse_obj(json_resp["Response"])


def get_appointment(appointment_id) -> GetAppointmentResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAppointment", id=appointment_id)
    json_resp = xmltodict.parse(resp.content)
    return GetAppointmentResponse.parse_obj(json_resp["Response"])


def remove_appointment(appointment_id) -> None:
    api = OnlineAfsprakenAPI()
    api.get("removeAppointment", id=appointment_id)
    return None


def set_appointment(
    agenda_id,
    start_time,
    date,
    customer_id,
    appointment_type_id,
    end_time=None,
    appointment_id=None,
    name=None,
    description=None,
    booking_mode=None,
) -> SetAppointmentResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "setAppointment",
        id=appointment_id,
        agendaId=agenda_id,
        startTime=start_time,
        date=date,
        customerId=customer_id,
        appointmentTypeId=appointment_type_id,
        endTime=end_time,
        name=name,
        description=description,
        bookingMode=booking_mode,
    )
    json_resp = xmltodict.parse(resp.content)
    return SetAppointmentResponse.parse_obj(json_resp["Response"])
