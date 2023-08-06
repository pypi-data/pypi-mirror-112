from typing import Dict, Optional

from onlineafspraken.schema.response import BaseResponseContent, OnlineAfsprakenBase


class BookableDaySchema(OnlineAfsprakenBase):
    date: int
    month: int
    day: int


class BookableTimeSchema(OnlineAfsprakenBase):
    date: int
    start_time: int
    end_time: int
    timestamp: int
    appointment_type_id: int
    resource_id: int


class GetBookableDaysResponse(BaseResponseContent):
    objects: Optional[Dict[str, BookableDaySchema]]


class GetBookableTimesResponse(BaseResponseContent):
    objects: Optional[Dict[str, BookableTimeSchema]]
