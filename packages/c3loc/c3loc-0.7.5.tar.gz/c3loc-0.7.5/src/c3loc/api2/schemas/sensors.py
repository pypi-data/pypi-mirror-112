from __future__ import annotations
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, validator  # type: ignore

from .types import DbInteger, SensorType, SensorValueType


class Sensors(BaseModel):
    tag_id: DbInteger
    ts: datetime
    type: int
    value: SensorValueType

    @classmethod
    def from_row(cls, row):
        vals = dict(row)
        typ: SensorType = vals['type']
        if typ == SensorType.SensorDataTemp:
            return SensorDataTemp(**vals)
        if typ == SensorType.SensorDataHumid:
            return SensorDataHumid(**vals)
        return None


class SensorDataTemp(BaseModel):
    tag_id: DbInteger
    ts: datetime
    value: float
    sensor_type = Field(default='SensorDataTemp', const=True)
    repr: Optional[str]

    @validator('value', pre=True)
    def convert_val(cls, v):
        return int.from_bytes(v, 'little', signed=True) / 10.0

    @validator('repr', always=True)
    def gen_repr(cls, v: Optional[str], values) -> str:
        if not v:
            return f'{values["value"]} ℃'
        return v


class SensorDataHumid(BaseModel):
    tag_id: DbInteger
    ts: datetime
    value: int
    sensor_type = Field(default='SensorDataHumid', const=True)
    repr: Optional[str]

    @validator('value', pre=True)
    def convert_val(cls, v):
        return int.from_bytes(v, 'little', signed=False)

    @validator('repr', always=True)
    def gen_repr(cls, v: Optional[str], values) -> str:
        if not v:
            return f'{values["value"]}% RH'
        return v


AnySensor = Union[SensorDataTemp, SensorDataHumid]
