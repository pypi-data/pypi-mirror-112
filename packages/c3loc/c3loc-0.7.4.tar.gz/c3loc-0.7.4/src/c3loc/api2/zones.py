from typing import Iterable

import fastapi  # type: ignore
from fastapi import Depends, APIRouter, Request
import sqlalchemy as sa  # type: ignore
from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore

from ..db_next import zones, get_db
from .schemas.zones import Zone, ZoneCreate, ZonePatch

router = APIRouter()


@router.get('/zones', response_model=Iterable[Zone])
async def get_zones(db: AsyncConnection = Depends(get_db)):
    return await db.execute(sa.select(zones))


@router.post('/zones')
async def create_zone(zone: ZoneCreate, request: Request,
                      db: AsyncConnection = Depends(get_db)):
    insert = zones.insert().values(zone.dict())
    result = await db.execute(insert)
    new_id = result.inserted_primary_key[0]
    root_path = request.scope.get("root_path")
    return fastapi.Response(status_code=201, headers={
        'Location': f'{root_path}/zones/{new_id}'})


@router.get('/zones/{zone_id}', response_model=Zone)
async def get_zone(zone_id: int, db: AsyncConnection = Depends(get_db)):
    result = await db.execute(zones.select().where(zones.c.id == zone_id))
    entry = result.first()
    if not entry:
        raise fastapi.HTTPException(404)
    return entry


@router.delete('/zones/{zone_id}')
async def delete_zone(zone_id: int, db: AsyncConnection = Depends(get_db)):
    result = await db.execute(zones.delete().where(zones.c.id == zone_id))
    if result.rowcount == 0:
        raise fastapi.HTTPException(404)
    return fastapi.Response(status_code=204)


@router.patch('/zones/{zone_id}')
async def patch_zone(zone_id: int, zone_updates: ZonePatch,
                     db: AsyncConnection = Depends(get_db)):
    result = await db.execute(zones.update().values(
        zone_updates.dict()).where(zones.c.id == zone_id))
    if result.rowcount == 0:
        raise fastapi.HTTPException(404)
    return fastapi.Response(status_code=204)
