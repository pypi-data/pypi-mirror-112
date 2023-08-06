from typing import Iterable

from fastapi import APIRouter, Depends, Response  # type: ignore
import jinja2
import sqlalchemy as sa  # type: ignore
from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore

from ..db_next import get_db, tags, zones
import c3loc.api2.queries as q
from .dependencies import make_paginator, tag_filters
from .schemas.proximity import Proximity

router = APIRouter()


@router.get('/proximity', response_model=Iterable[Proximity])
async def proximity(db: AsyncConnection = Depends(get_db),
                    p=Depends(make_paginator),
                    filt=Depends(tag_filters)):
    result = await db.execute(p(filt(q.proximity())))
    return result

XML_TEMPLATE = jinja2.Template("""<?xml version="1.0" encoding="UTF-8"?>
<TagData>
  {%- for tag in tags %}
  <Tag id="{{ tag.id }}">
    <Name>{{ tag.name }}</Name>
    {%- if tag.zone_id %}
    <Location>{{ tag.zone_name }}</Location>
    <LocationId>{{ tag.zone_id }}</LocationId>
    <LastSeen>{{ tag.last_seen }}</LastSeen>
    <Distance>{{ tag.distance }}</Distance>
    {%- else %}
    <Location>Unknown</Location>
    {%- endif %}
  </Tag>
  {%- endfor %}
</TagData>
""")


@router.get('/proximity.xml')
async def proximity_xml(db: AsyncConnection = Depends(get_db)):
    query = sa.select(
        [tags.c.distance, zones.c.name.label('zone_name'),
         tags.c.name, tags.c.last_seen,
         tags.c.id, tags.c.zone_id, tags.c.alarm_active]
    ).select_from(tags.outerjoin(zones)).where(
        tags.c.type.in_(['SmartRelay', 'SecureSmartRelay'])
    ).order_by(tags.c.id.asc())
    results = (dict(r) for r in await db.execute(query))
    return Response(
        content=XML_TEMPLATE.render(tags=[dict(r) for r in results]),
        status_code=200, headers={'Content-Type': 'text/xml'})
