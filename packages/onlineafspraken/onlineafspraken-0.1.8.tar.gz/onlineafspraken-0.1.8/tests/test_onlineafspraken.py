#!/usr/bin/env python

"""Tests for `onlineafspraken` package."""
import pytest
import respx
from httpx import Response

from onlineafspraken.api.appointment import set_appointment
from onlineafspraken.api.availability import get_bookable_days, get_bookable_times
from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.api.customers import set_customer, get_customer, get_customers
from onlineafspraken.api.general import get_agendas, get_appointment_types, get_agenda
from onlineafspraken.schema.general import GetAgendasResponse


@pytest.fixture
def mock_get_agendas():
    api = OnlineAfsprakenAPI()

    with respx.mock(base_url=api.get_base_url(), assert_all_called=False) as mock:
        route = mock.get(params=api.set_params("getAgendas"), name="get_agendas")
        mock_resp_content = """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Status>
                <APIVersion>1.0</APIVersion>
                <Date>2021-06-25 14:09:13</Date>
                <Timestamp>1624622953</Timestamp>
                <Status>success</Status>
            </Status>
            <Objects>
                <Agenda>
                    <Id>32492</Id>
                    <Name></Name>
                    <DateFormat>D d/m/Y</DateFormat>
                    <TimeFormat>H:i</TimeFormat>
                    <AlignGrid>5</AlignGrid>
                    <IsDefault>1</IsDefault>
                </Agenda>
            </Objects>
        </Response>
        """
        route.return_value = Response(200, text=mock_resp_content)
        yield mock


def test_get_agendas_200(mock_get_agendas):
    response = get_agendas()
    assert mock_get_agendas["get_agendas"].called
    assert response.status.status == "success"
    assert isinstance(response, GetAgendasResponse)


def test_get_agenda():
    at = get_agenda(32492)
    pass


def test_get_appointment_types():
    at = get_appointment_types()
    pass


def test_get_bookable_days():
    bd = get_bookable_days(32492, 346655, "2021-07-12", "2021-12-31")
    pass


def test_get_bookable_times():
    bd = get_bookable_times(32492, 346655, "2021-07-13")
    pass


def test_set_customer():
    c = set_customer("john", "doe", "johbdoe@test.com")
    pass


def test_get_customers():
    c = get_customers()
    pass


def test_get_customer():
    c = get_customer(26142790)
    pass


def test_set_appointment():
    ap = set_appointment(32492, "10:00", "2021-07-15", 26142790, 346655)
    pass
