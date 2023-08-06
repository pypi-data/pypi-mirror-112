import xmltodict

from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.schema.customer import (
    GetCustomerResponse,
    GetCustomersResponse,
    GetFieldsResponse,
    PasswordRecoveryResponse,
    SetCustomerResponse,
)


def get_customer(customer_id) -> GetCustomerResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("getCustomer", id=customer_id)
    json_resp = xmltodict.parse(resp.content)
    return GetCustomerResponse.parse_obj(json_resp["Response"])


def get_customers(
    limit=None,
    offset=None,
    update_after=None,
    email=None,
    birth_date=None,
    account_number=None,
) -> GetCustomersResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "getCustomers",
        limit=limit,
        offset=offset,
        updateAfter=update_after,
        email=email,
        birthDate=birth_date,
        accountNumber=account_number,
    )
    json_resp = xmltodict.parse(resp.content)
    return GetCustomersResponse.parse_obj(json_resp["Response"])


def get_fields(agenda_id, appointment_type_id=None) -> GetFieldsResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "getFields", agendaId=agenda_id, appointmentTypeId=appointment_type_id
    )
    json_resp = xmltodict.parse(resp.content)
    return GetFieldsResponse.parse_obj(json_resp["Response"])


def login_customer(username, password) -> GetCustomerResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("loginCustomer", username=username, password=password)
    json_resp = xmltodict.parse(resp.content)
    return GetCustomerResponse.parse_obj(json_resp["Response"])


def login_customer_with_facebook(facebook_id) -> GetCustomerResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("loginCustomerWithFacebook", facebookId=facebook_id)
    json_resp = xmltodict.parse(resp.content)
    return GetCustomerResponse.parse_obj(json_resp["Response"])


def password_recovery(email) -> PasswordRecoveryResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get("passwordRecovery", email=email)
    json_resp = xmltodict.parse(resp.content)
    return PasswordRecoveryResponse.parse_obj(json_resp["Response"])


def set_customer(
    first_name: str,
    last_name: str,
    email: str,
    customer_id: int = None,
    account_number: int = None,
    phone: str = None,
    mobile_phone: str = None,
    insertions: str = None,
    birth_date: str = None,
    gender: str = None,
    street: str = None,
    house_nr: int = None,
    house_nr_addition: str = None,
    zip_code: str = None,
    city: str = None,
    country: str = None,
    status: int = None,
) -> SetCustomerResponse:
    api = OnlineAfsprakenAPI()
    resp = api.get(
        "setCustomer",
        firstName=first_name,
        lastName=last_name,
        email=email,
        id=customer_id,
        accountNumber=account_number,
        phone=phone,
        mobilePhone=mobile_phone,
        insertions=insertions,
        birthDate=birth_date,
        gender=gender,
        street=street,
        houseNr=house_nr,
        houseNrAddition=house_nr_addition,
        zipCode=zip_code,
        city=city,
        country=country,
        status=status,
    )
    json_resp = xmltodict.parse(resp.content)
    return SetCustomerResponse.parse_obj(json_resp["Response"])
