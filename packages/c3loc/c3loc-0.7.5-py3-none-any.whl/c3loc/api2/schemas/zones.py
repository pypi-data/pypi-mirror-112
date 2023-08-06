from pydantic import BaseModel  # type: ignore


class ZoneCreate(BaseModel):
    name: str


class Zone(ZoneCreate):
    id: int


class ZonePatch(ZoneCreate):
    pass
