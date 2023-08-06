from typing import Callable, Iterable

import fastapi  # type: ignore
from fastapi import Depends, APIRouter  # type: ignore
import sqlalchemy as sa  # type: ignore
from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore

from ..db_next import alarms, get_db
import c3loc.api2.queries as q
from .dependencies import make_paginator
from .schemas.alarms import Alarm, AlarmPatch

router = APIRouter()


@router.get('/alarms', response_model=Iterable[Alarm])
async def get_alarms(db: AsyncConnection = Depends(get_db),
                     p: Callable = Depends(make_paginator)):
    query = q.get_alarms()
    result = await db.execute(p(query))
    return result


@router.get('/alarms/{alarm_id}', response_model=Alarm)
async def get_alarm(alarm_id: int, db: AsyncConnection = Depends(get_db)):
    result = await db.execute(q.get_alarm(alarm_id))
    entry = result.first()
    if not entry:
        raise fastapi.HTTPException(404)
    return entry


@router.patch('/alarms/{alarm_id}')
async def patch_alarm(alarm_id: int, alarm_updates: AlarmPatch,
                      db: AsyncConnection = Depends(get_db)):
    result = await db.execute(alarms.select().where(alarms.c.id == alarm_id))
    entry = result.first()
    if not entry:
        raise fastapi.HTTPException(404)
    if alarm_updates.acknowledged and not entry['ack_ts']:
        await db.execute(alarms.update().values(
            ack_ts=sa.func.now()).where(alarms.c.id == alarm_id))
    return fastapi.Response(status_code=204)
