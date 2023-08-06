from typing import Iterable

import fastapi  # type: ignore
from fastapi import Depends, APIRouter
import sqlalchemy as sa  # type: ignore
from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore

from ..db_next import listeners, get_db
from .dependencies import make_paginator
from .schemas.listeners import Listener, ListenerPatch

router = APIRouter()


@router.get('/listeners', response_model=Iterable[Listener])
async def get_listeners(db: AsyncConnection = Depends(get_db),
                        p=Depends(make_paginator)):
    return await db.execute(p(sa.select(listeners)))


@router.get('/listeners/{listener_id}', response_model=Listener)
async def get_listener(listener_id: str,
                       db: AsyncConnection = Depends(get_db)):
    result = await db.execute(
        listeners.select().where(listeners.c.id == listener_id))
    entry = result.first()
    if not entry:
        raise fastapi.HTTPException(404)
    return entry


@router.patch('/listeners/{listener_id}')
async def patch_listener(listener_id: str, listener_updates: ListenerPatch,
                         db: AsyncConnection = Depends(get_db)):
    result = await db.execute(listeners.update().values(
        listener_updates.dict()).where(listeners.c.id == listener_id))
    if result.rowcount == 0:
        raise fastapi.HTTPException(404)
    return fastapi.Response(status_code=204)
