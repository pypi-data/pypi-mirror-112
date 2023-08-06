from typing import Callable, Iterable

import fastapi  # type: ignore
from fastapi import Depends, APIRouter, Request
import sqlalchemy as sa  # type: ignore
from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore

from ..db_next import groups, get_db
from .dependencies import make_paginator
from .schemas.groups import Group, GroupCreate, GroupPatch

router = APIRouter()


@router.get('/groups', response_model=Iterable[Group])
async def get_groups(db: AsyncConnection = Depends(get_db),
                     p: Callable = Depends(make_paginator)):
    return await db.execute(p(sa.select(groups)))


@router.post('/groups')
async def create_group(group: GroupCreate, request: Request,
                       db: AsyncConnection = Depends(get_db)):
    insert = groups.insert().values(group.dict())
    result = await db.execute(insert)
    new_id = result.inserted_primary_key[0]
    root_path = request.scope.get("root_path")
    return fastapi.Response(status_code=201, headers={
        'Location': f'{root_path}/groups/{new_id}'})


@router.get('/groups/{group_id}', response_model=Group)
async def get_group(group_id: int, db: AsyncConnection = Depends(get_db)):
    result = await db.execute(groups.select().where(groups.c.id == group_id))
    entry = result.first()
    if not entry:
        raise fastapi.HTTPException(404)
    return entry


@router.delete('/groups/{group_id}')
async def delete_group(group_id: int, db: AsyncConnection = Depends(get_db)):
    result = await db.execute(groups.delete().where(groups.c.id == group_id))
    if result.rowcount == 0:
        raise fastapi.HTTPException(404)
    return fastapi.Response(status_code=204)


@router.patch('/groups/{group_id}')
async def patch_group(group_id: int, group_updates: GroupPatch,
                      db: AsyncConnection = Depends(get_db)):
    result = await db.execute(groups.update().values(
        group_updates.dict()).where(groups.c.id == group_id))
    if result.rowcount == 0:
        raise fastapi.HTTPException(404)
    return fastapi.Response(status_code=204)
