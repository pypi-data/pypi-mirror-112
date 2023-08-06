from datetime import datetime, timedelta
import json

from aiohttp import web
from aiohttp_cors import CorsViewMixin  # type: ignore
import asyncpg  # type: ignore
from dateutil.parser import isoparse
from marshmallow import EXCLUDE
import pytz

from ..config import CONFIG
from .schemas import (ibeacon_post_schema, macbeacon_post_schema,
                      tag_patch_schema, history_schema, contacts_schema,
                      secure_beacon_post_schema)
from .sensors import format_sensors
from .views import ValidatingView, paginate_query


def tag_schema_dump(row):
    if row['type'] in {'iBeacon', 'LocationAnchor'}:
        return ibeacon_post_schema.dump(row)
    if row['type'] in {'SecureLocationAnchor', 'SecureSmartRelay'}:
        return secure_beacon_post_schema.dump(row)
    return macbeacon_post_schema.dump(row)


class TagsView(ValidatingView):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = None
            if 'type' in self.request.query:
                query = ('SELECT * from tags WHERE type = $1',
                         self.request.query['type'])
            elif 'group_id' in self.request.query:
                try:
                    query = ('SELECT * from tags WHERE group_id = $1',
                             int(self.request.query['group_id']))
                except ValueError:
                    raise web.HTTPBadRequest(text='bad group_id')
            else:
                query = ('SELECT * from tags', )
            query = paginate_query(self.request, query)
            try:
                tags = await conn.fetch(*query)
            except asyncpg.exceptions.InvalidTextRepresentationError:
                raise web.HTTPBadRequest(text='Invalid tag type')
            return web.json_response(
                [tag_schema_dump(r) for r in tags if r is not None])

    async def post(self):
        body = await self._valid_json(self.request)

        if 'type' not in body:
            raise web.HTTPBadRequest(reason='Type field is required for post')

        new_t = {}
        if body['type'] in {'iBeacon', 'LocationAnchor'}:
            new_t.update(self._validate(ibeacon_post_schema, body))
        elif body['type'] == 'SmartRelay':
            new_t.update(self._validate(macbeacon_post_schema, body))
        elif body['type'] in {'SecureSmartRelay', 'SecureLocationAnchor'}:
            new_t.update(self._validate(secure_beacon_post_schema, body))
        else:
            raise web.HTTPBadRequest(reason=f'Unknown tag type {body["type"]}')

        async with self.request.app['db_pool'].acquire() as conn:
            try:
                await conn.execute(
                    'INSERT INTO tags '
                    '(mac, uuid, major, minor, type, zone_id, name, '
                    'group_id, bid, attrs) VALUES '
                    '($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
                    new_t.get('mac', None),
                    new_t.get('uuid', None),
                    new_t.get('major', None),
                    new_t.get('minor', None),
                    new_t['type'],
                    new_t.get('zone_id', None),
                    new_t.get('name', None),
                    new_t.get('group_id', None),
                    new_t.get('bid', None),
                    json.dumps(new_t.get('attrs', {})))
            except asyncpg.exceptions.UniqueViolationError as e:
                raise web.HTTPConflict(reason=str(e.detail))
            except (asyncpg.exceptions.InvalidTextRepresentationError,
                    asyncpg.exceptions.NotNullViolationError,
                    asyncpg.exceptions.ForeignKeyViolationError) as e:
                raise web.HTTPBadRequest(reason=str(e.detail))
        raise web.HTTPCreated


def parse_start_end(request):
    utc = pytz.timezone('UTC')
    if 'start' in request.query:
        try:
            start = isoparse(request.query['start'])
        except ValueError:
            raise web.HTTPBadRequest(
                reason="Invailid ISO8601 in start parameter")
        if start.tzinfo:
            start = start.astimezone(utc).replace(tzinfo=None)
    else:
        start = datetime.utcnow() - timedelta(days=7)

    if 'end' in request.query:
        try:
            end = isoparse(request.query['end'])
        except ValueError:
            raise web.HTTPBadRequest(
                reason="Invailid ISO8601 in end parameter")
        if end.tzinfo:
            end = end.astimezone(utc).replace(tzinfo=None)
    else:
        end = datetime.max

    return start, end


HISTORY_QUERY = """
SELECT tag_id,
       zone_id,
       start_ts,
       distance,
       coalesce(end_ts, (now() at time zone 'utc'))            as end_ts,
       coalesce(end_ts, (now() at time zone 'utc')) - start_ts as duration
FROM history
WHERE tag_id = $1 AND tsrange(start_ts, end_ts) && tsrange($2, $3)
ORDER BY start_ts DESC
"""  # noqa: E501


class TagHistoryView(web.View, CorsViewMixin):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        start, end = parse_start_end(self.request)
        async with self.request.app['db_pool'].acquire() as conn:
            query = (HISTORY_QUERY, t_id, start, end)
            query = paginate_query(self.request, query)
            history = await conn.fetch(*query)
            return web.json_response(history_schema.dump(history))


CONTACT_QUERY = """
with target_tag as (
    SELECT tag_id, start_ts, end_ts, zone_id
    from history
    where tag_id = $1
      and tsrange(start_ts, end_ts) && tsrange($2, $3)
),
     other_tag as (
         SELECT tag_id, start_ts, end_ts, zone_id
         from history
         where tag_id != $1
           and tsrange(start_ts, end_ts) && tsrange($2, $3)
     ),
     overlap as (
         SELECT other_tag.tag_id,
                greatest(target_tag.start_ts, other_tag.start_ts)                                as start_ts,
                least(coalesce(target_tag.end_ts, (now() at time zone 'utc')), other_tag.end_ts) as end_ts,
                other_tag.zone_id                                                                as zone_id,
                least(coalesce(target_tag.end_ts, (now() at time zone 'utc')), other_tag.end_ts) -
                greatest(target_tag.start_ts, other_tag.start_ts)                                as duration
         from target_tag,
              other_tag
         where target_tag.zone_id = other_tag.zone_id
           and tsrange(target_tag.start_ts, target_tag.end_ts) && tsrange(other_tag.start_ts, other_tag.end_ts)
     )
SELECT overlap.*,
       zones.name as zone_name,
       tags.name as tag_name,
       md5(concat($1::text, tag_id::text, overlap.zone_id, start_ts::text, end_ts::text)) as hash
from overlap
         join tags on tag_id = tags.id
         join zones on zones.id = overlap.zone_id
         order by start_ts desc
"""  # noqa: E501


async def tag_exists_or_404(t_id: int, conn) -> None:
    tag_exists = await conn.fetchval(
        "SELECT id from tags where id = $1", t_id)
    if not tag_exists:
        raise web.HTTPNotFound


class TagContactView(web.View, CorsViewMixin):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        start, end = parse_start_end(self.request)
        async with self.request.app['db_pool'].acquire() as conn:
            await tag_exists_or_404(t_id, conn)
            query = (CONTACT_QUERY, t_id, start, end)
            max_limit = int(CONFIG['API_RESULT_LIMIT_CONTACTS'])
            query = paginate_query(self.request, query, max_limit=max_limit)
            contacts = await conn.fetch(*query)
            return web.json_response(contacts_schema.dump(contacts))


SENSORS_QUERY = """
SELECT * FROM sensors
WHERE tag_id = $1 AND ts >= $2 AND ts <= $3 ORDER BY ts DESC
"""


class TagSensorView(web.View, CorsViewMixin):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        start, end = parse_start_end(self.request)
        async with self.request.app['db_pool'].acquire() as conn:
            await tag_exists_or_404(t_id, conn)
            query = (SENSORS_QUERY, t_id, start, end)
            query = paginate_query(self.request, query)
            sensors = await conn.fetch(*query)
            return web.json_response(format_sensors(sensors))


class TagView(ValidatingView):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            tag = await conn.fetchrow(
                'SELECT * FROM tags t WHERE id = $1', t_id)
            if not tag:
                raise web.HTTPNotFound
            return web.json_response(tag_schema_dump(tag))

    async def patch(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM tags t WHERE id = $1', t_id)
            if not row:
                raise web.HTTPNotFound
            tag = dict(row.items())
            body = await self._valid_json(self.request)
            updates = self._validate(tag_patch_schema, body)
            if 'type' in updates:
                # Ensure that we are validating against existing type
                del body['type']
            tag.update(updates)
            if tag['type'] in {'iBeacon', 'LocationAnchor'}:
                self._validate(ibeacon_post_schema, tag, unknown=EXCLUDE)
            elif tag['type'] == 'SmartRelay':
                self._validate(macbeacon_post_schema, tag, unknown=EXCLUDE)
            elif tag['type'] in {'SecureSmartRelay', 'SecureLocationAnchor'}:
                self._validate(secure_beacon_post_schema, tag, unknown=EXCLUDE)
            else:
                raise web.HTTPBadRequest(
                    reason=f'Unknown tag type {body["type"]}')
            await conn.execute(
                'UPDATE tags SET name = $1, mac = $2, uuid = $3, major = $4, '
                'minor = $5, attrs = $6, zone_id = $7, group_id = $8, '
                'bid = $9 WHERE id = $10', tag['name'], tag['mac'],
                tag['uuid'], tag['major'], tag['minor'],
                json.dumps(tag['attrs']), tag['zone_id'], tag['group_id'],
                tag['bid'], t_id)
        raise web.HTTPNoContent

    async def delete(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            await conn.execute('DELETE from tags where id = $1', t_id)
        raise web.HTTPNoContent
