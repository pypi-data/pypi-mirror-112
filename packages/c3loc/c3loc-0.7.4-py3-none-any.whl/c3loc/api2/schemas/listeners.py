from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, root_validator  # type: ignore

from .types import DbInteger, Attributes


class ListenerBase(BaseModel):
    zone_id: Optional[DbInteger]
    attrs: Optional[Attributes] = {}


class Listener(ListenerBase):
    id: str
    last_seen: datetime
    name: Optional[str]

    @root_validator
    def default_name(cls, values: Dict) -> Dict:
        if values.get('name', None):
            return values
        values['name'] = f'Listener {values["id"]}'
        return values


class ListenerPatch(ListenerBase):
    pass
