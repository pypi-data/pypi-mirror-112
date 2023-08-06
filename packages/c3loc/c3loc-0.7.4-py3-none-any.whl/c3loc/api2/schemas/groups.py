from pydantic import BaseModel  # type: ignore


class GroupCreate(BaseModel):
    name: str


class Group(GroupCreate):
    id: int


class GroupPatch(GroupCreate):
    pass
