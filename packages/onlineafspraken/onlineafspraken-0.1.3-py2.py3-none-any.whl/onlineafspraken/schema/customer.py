from typing import Optional, Dict

from onlineafspraken.schema.response import OnlineAfsprakenBase, BaseResponseContent


class CustomerSchema(OnlineAfsprakenBase):
    id: int
    account_number: int
    first_name: str
    last_name: str
    insertions: str
    birth_date: str
    gender: str
    street: str
    house_nr: int
    house_nr_addition: str
    zip_code: str
    city: str
    country: str
    phone: str
    mobile_phone: str
    email: str
    status: int
    update_time: str
    create_time: str


class SetCustomerSchema(OnlineAfsprakenBase):
    id: int
    status: int


class FieldsSchema(OnlineAfsprakenBase):
    id: int
    label: str
    key: str
    type: str
    required: int


class PasswordRecoverySchema(OnlineAfsprakenBase):
    message: str


class SetCustomerResponse(BaseResponseContent):
    data: SetCustomerSchema


class PasswordRecoveryResponse(BaseResponseContent):
    data: CustomerSchema


class GetCustomerResponse(BaseResponseContent):
    data: CustomerSchema


class GetCustomersResponse(BaseResponseContent):
    objects: Optional[Dict[str, CustomerSchema]]


class GetFieldsResponse(BaseResponseContent):
    objects: Optional[Dict[str, FieldsSchema]]
