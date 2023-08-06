from typing import Iterable

from fastapi import APIRouter, Depends  # type: ignore
from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore

from ..db_next import get_db
import c3loc.api2.queries as q
from .dependencies import make_paginator
from .schemas.sensors import Sensors, AnySensor

router = APIRouter()


@router.get('/sensors', response_model=Iterable[AnySensor])
async def sensors(db: AsyncConnection = Depends(get_db),
                  p=Depends(make_paginator)):
    result = await db.execute(p(q.get_sensors()))
    return (i for i in (Sensors.from_row(r) for r in result) if i)
