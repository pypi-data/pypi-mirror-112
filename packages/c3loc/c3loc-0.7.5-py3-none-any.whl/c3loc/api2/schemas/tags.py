import re
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, Type, Union
from uuid import UUID

from pydantic import (  # type: ignore
    BaseModel, ConstrainedStr, Field, root_validator,
    validator)

from ...config import CONFIG
from .types import DbInteger, Unsigned16Bit, Unsigned32Bit


class TagType(str, Enum):
    SmartRelay = 'SmartRelay'
    SecureSmartRelay = 'SecureSmartRelay'
    LocationAnchor = 'LocationAnchor'
    IBeacon = 'iBeacon'


class TagBase(BaseModel):
    type: TagType
    name: Optional[str]
    zone_id: Optional[DbInteger]
    group_id: Optional[DbInteger]
    attrs: Optional[Dict[str, Union[str, int]]] = {}


class MacAddress(ConstrainedStr):
    regex = re.compile(
        r'^[a-fA-F0-9]{2}:[a-fA-F0-9]{2}:[a-fA-F0-9]{2}:'
        r'[a-fA-F0-9]{2}:[a-fA-F0-9]{2}:[a-fA-F0-9]{2}$')


class TagCreate(TagBase):
    uuid: Optional[UUID]
    major: Optional[Unsigned16Bit]
    minor: Optional[Unsigned16Bit]
    mac: Optional[MacAddress]
    bid: Optional[Unsigned32Bit]


class Tag(TagBase):
    last_seen: datetime
    zone_start: datetime
    battery_pct: Optional[int]
    alarm_active: bool


class IBeacon(TagBase):
    uuid: UUID
    major: Unsigned16Bit
    minor: Unsigned16Bit
    type: TagType = Field(default=TagType.IBeacon, const=True)

    @root_validator
    def default_name(cls, values: Dict) -> Dict:
        if values['name']:
            return values
        uuid = values['uuid']
        major = values['major']
        minor = values['minor']
        if uuid == CONFIG['LA_UUID']:
            values['name'] = f'LocationAnchor {uuid}:{major}:{minor}'
        else:
            values['name'] = f'iBeacon {uuid}:{major}:{minor}'
        return values


class SmartRelay(TagBase):
    mac: MacAddress = Field(...,)
    type: TagType = Field(default=TagType.SmartRelay, const=True)

    @root_validator
    def default_name(cls, values: Dict) -> Dict:
        if values['name']:
            return values
        values['name'] = f'SmartRelay {values["mac"]}'
        return values


class SecureSmartRelay(TagBase):
    bid: Unsigned32Bit
    type: TagType = Field(default=TagType.SecureSmartRelay, const=True)

    @root_validator
    def default_name(cls, values: Dict) -> Dict:
        if values['name']:
            return values
        values['name'] = f'SecureSmartRelay {hex(values["bid"])}'
        return values


class TagPatch(BaseModel):
    name: Optional[str]
    zone_id: Optional[DbInteger]
    group_id: Optional[DbInteger]
    attrs: Optional[Dict[str, Union[str, int]]] = {}


def dispatch_model(create: TagCreate):
    map: Dict[TagType, Type[BaseModel]] = {
        TagType.IBeacon: IBeacon,
        TagType.SecureSmartRelay: SecureSmartRelay,
        TagType.SmartRelay: SmartRelay}

    return map[create.type].parse_obj(create.dict())


class TagHistory(BaseModel):
    zone_id: DbInteger
    start_ts: datetime
    end_ts: Optional[datetime] = None
    distance: float
    duration: Optional[timedelta] = None
    zone_name: Optional[str]

    @validator('end_ts', always=True)
    def default_end_ts(cls, v: datetime) -> datetime:
        if v:
            return v
        return datetime.utcnow()

    @validator('duration', always=True)
    def calc_duration(cls, _, values):
        return values['end_ts'] - values['start_ts']


class TagContact(BaseModel):
    tag_id: DbInteger
    tag_name: str
    end_ts: datetime
    start_ts: datetime
    duration: Optional[timedelta] = None
    zone_id: DbInteger
    zone_name: str
    hash: str

    @validator('duration', always=True)
    def calc_duration(cls, _, values):
        return values['end_ts'] - values['start_ts']
