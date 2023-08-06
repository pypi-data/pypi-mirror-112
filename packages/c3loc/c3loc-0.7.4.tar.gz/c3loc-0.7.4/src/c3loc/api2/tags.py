from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore
from typing import Iterable

from fastapi import (  # type: ignore
    APIRouter, Depends, HTTPException, Request, Response)
from pydantic import ValidationError  # type: ignore

from ..db_next import get_db, tags, history
from .dependencies import (make_paginator, tag_filters, time_filters,
                           make_contacts_paginator, bindable_time_filter)
import c3loc.api2.queries as q
from .schemas.tags import (Tag, TagContact, TagCreate, TagHistory, TagPatch,
                           dispatch_model)


router = APIRouter()


@router.post('/tags')
async def create_tag(new_tag: TagCreate, request: Request,
                     db: AsyncConnection = Depends(get_db)):
    try:
        new_tag = dispatch_model(new_tag)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.json())
    insert = tags.insert().values(new_tag.dict())
    result = await db.execute(insert)
    new_id = result.inserted_primary_key[0]
    root_path = request.scope.get("root_path")
    return Response(status_code=201, headers={
        'Location': f'{root_path}/tags/{new_id}'})


@router.get('/tags', response_model=Iterable[Tag])
async def get_tags(db: AsyncConnection = Depends(get_db),
                   p=Depends(make_paginator),
                   filt=Depends(tag_filters)):
    result = await db.execute(p(filt(q.get_tags())))
    return result


@router.delete('/tags/{tag_id}')
async def delete_tag(tag_id: int, db: AsyncConnection = Depends(get_db)):
    result = await db.execute(tags.delete().where(tags.c.id == tag_id))
    if result.rowcount == 0:
        raise HTTPException(404)
    return Response(status_code=204)


@router.get('/tags/{tag_id}', response_model=Tag)
async def get_tag(tag_id: int, db: AsyncConnection = Depends(get_db)):
    entry = await q.get_or_404(db, tags, tag_id)
    return entry


@router.patch('/tags/{tag_id}')
async def patch_tag(tag_id: int, tag_updates: TagPatch,
                    db: AsyncConnection = Depends(get_db)):
    await q.get_or_404(db, tags, tag_id)
    await db.execute(
        tags.update().values(tag_updates.dict()).where(tags.c.id == tag_id))
    return Response(status_code=204)


@router.get('/tags/{tag_id}/history', response_model=Iterable[TagHistory])
async def tag_history(tag_id: int,
                      db: AsyncConnection = Depends(get_db),
                      p=Depends(make_paginator),
                      t=Depends(time_filters)):
    await q.get_or_404(db, tags, tag_id)
    query = q.get_history(tag_id)
    query = t(query, history.c.start_ts, history.c.end_ts)
    return (TagHistory.parse_obj(r) for r in await db.execute(p(query)))


@router.get('/tags/{tag_id}/contacts', response_model=Iterable[TagContact])
async def tag_contacts(tag_id: int,
                       db: AsyncConnection = Depends(get_db),
                       p=Depends(make_contacts_paginator),
                       t=Depends(bindable_time_filter)):
    await q.get_or_404(db, tags, tag_id)
    query = q.get_contacts(tag_id)
    print(query)
    query = t(query)
    print(query)
    query = p(query)
    print(query)
    results = await db.execute(query)
    return (TagContact.parse_obj(r) for r in results)
