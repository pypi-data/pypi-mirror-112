#!/usr/bin/env python

"""Tests for `onlineafspraken` package."""
import pytest
import respx
from httpx import Response

from onlineafspraken.api.client import OnlineAfsprakenAPI
from onlineafspraken.api.general import get_agendas
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
