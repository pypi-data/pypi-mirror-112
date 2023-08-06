import xmltodict

from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.schema.general import (
    GetAgendaResponse,
    GetAgendasResponse,
    GetAppointmentTypeResponse,
    GetAppointmentTypesResponse,
    GetResourceResponse,
    GetResourcesResponse,
    RequiresConfirmationResponse,
)


def get_agenda(agenda_id) -> GetAgendaResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAgenda", id=agenda_id)
    json_resp = xmltodict.parse(resp.content)
    return GetAgendaResponse.parse_obj(json_resp["Response"])


def get_agendas() -> GetAgendasResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAgendas")
    json_resp = xmltodict.parse(resp.content)
    return GetAgendasResponse.parse_obj(json_resp["Response"])


def get_appointment_type(type_id) -> GetAppointmentTypeResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAppointmentType", id=type_id)
    json_resp = xmltodict.parse(resp.content)
    return GetAppointmentTypeResponse.parse_obj(json_resp["Response"])


def get_appointment_types():
    api = OnlineAfsprakenAPI()
    resp = api.get("getAppointmentTypes")
    json_resp = xmltodict.parse(resp.content)
    return GetAppointmentTypesResponse.parse_obj(json_resp["Response"])


def get_resource(resource_id) -> GetResourceResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getResource", id=resource_id)
    json_resp = xmltodict.parse(resp.content)
    return GetResourceResponse.parse_obj(json_resp["Response"])


def get_resources() -> GetResourcesResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getAppointmentType")
    json_resp = xmltodict.parse(resp.content)
    return GetResourcesResponse.parse_obj(json_resp["Response"])


def requires_confirmation() -> RequiresConfirmationResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("requiresConfirmation")
    json_resp = xmltodict.parse(resp.content)
    return RequiresConfirmationResponse.parse_obj(json_resp["Response"])
