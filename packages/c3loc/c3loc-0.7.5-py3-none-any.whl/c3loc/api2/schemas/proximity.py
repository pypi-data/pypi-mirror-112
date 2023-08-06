from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # type: ignore

from .types import DbInteger
from .tags import TagType


class Proximity(BaseModel):
    tag_id: DbInteger
    tag_name: str
    zone_name: Optional[str]
    last_seen: datetime
    tag_type: TagType
    distance: Optional[float]
    alarm_active: Optional[bool]
