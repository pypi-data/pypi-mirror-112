from datetime import datetime
from typing import Optional

import sqlalchemy as sa  # type: ignore
from dateutil.parser import isoparse
from fastapi import HTTPException
from pytz import utc

from ..config import CONFIG
from ..db_next import tags
from .schemas.tags import TagType
from .schemas.types import DbInteger

MAX_LIMIT: int = int(CONFIG['API_RESULT_LIMIT'])
CONTACTS_MAX_LIMIT: int = int(CONFIG['API_RESULT_LIMIT_CONTACTS'])


def make_paginator(limit: int = MAX_LIMIT, offset: int = 0):
    if limit < 0 or limit > MAX_LIMIT:
        limit = MAX_LIMIT
    offset = 0 if offset < 0 else offset

    def f(query):
        if offset:
            query = query.offset(offset)
        return query.limit(limit)
    return f


def make_contacts_paginator(limit: int = CONTACTS_MAX_LIMIT,
                            offset: int = 0):
    if limit < 0 or limit > CONTACTS_MAX_LIMIT:
        limit = CONTACTS_MAX_LIMIT
    offset = 0 if offset < 0 else offset

    def f(query):
        return query.bindparams(limit=limit, offset=offset)

    return f


def tag_filters(type: Optional[TagType] = None,
                group_id: Optional[DbInteger] = None):
    def f(query):
        if type:
            query = query.where(tags.c.type == type)
        if group_id:
            query = query.where(tags.c.group_id == group_id)
        return query
    return f


def bindable_time_filter(start: Optional[str] = None,
                         end: Optional[str] = None):
    def parse(x: Optional[str], name):
        if not x:
            return None
        try:
            y: datetime = isoparse(x)
        except ValueError:
            raise HTTPException(
                status_code=422, detail=f'Bad iso8601 in \'{name}\' parameter')
        if y.tzinfo:
            y = y.astimezone(utc).replace(tzinfo=None)
        return y

    s = parse(start, 'start')
    e = parse(end, 'end')

    def binder(text_expr):
        return text_expr.bindparams(start=s, end=e)
    return binder


def time_filters(start: Optional[str] = None,
                 end: Optional[str] = None):
    def parse(x: Optional[str], name):
        if not x:
            return None
        try:
            y: datetime = isoparse(x)
        except ValueError:
            raise HTTPException(
                status_code=422, detail=f'Bad iso8601 in \'{name}\' parameter')
        if y.tzinfo:
            y = y.astimezone(utc).replace(tzinfo=None)
        return y

    s = parse(start, 'start')
    e = parse(end, 'end')

    def f(query, start_field: Optional[sa.Column] = None,
          end_field: Optional[sa.Column] = None):
        if s and start_field is not None:
            query = query.where(start_field <= s)
        if e and end_field is not None:
            query = query.where(end_field >= e)
        return query
    return f
