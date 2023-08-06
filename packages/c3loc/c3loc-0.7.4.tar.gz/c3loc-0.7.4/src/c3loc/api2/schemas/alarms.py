from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # type: ignore


class AlarmLinks(BaseModel):
    tag: str
    zone: str


class Alarm(BaseModel):
    id: int
    tag_name: str
    zone_name: Optional[str]
    start_ts: datetime
    last_ts: datetime
    acknowledged: bool
    priority: int


class AlarmPatch(BaseModel):
    acknowledged: bool
