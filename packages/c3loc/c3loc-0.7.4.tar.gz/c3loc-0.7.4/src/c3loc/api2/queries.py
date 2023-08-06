import sqlalchemy as sa  # type: ignore
from sqlalchemy.ext.asyncio import AsyncConnection  # type: ignore
from fastapi import HTTPException

from ..db_next import alarms, history, sensors, tags, zones


def get_alarm(alarm_id: int) -> sa.sql.expression:
    return get_alarms().where(alarms.c.id == alarm_id)


def get_alarms() -> sa.sql.expression:
    return sa.select([alarms.c.id, tags.c.name.label('tag_name'),
                      zones.c.name.label('zone_name'),
                      alarms.c.start_ts, alarms.c.last_ts,
                      alarms.c.acknowledged, alarms.c.priority]).select_from(
        alarms.join(tags).outerjoin(zones))


def get_tags() -> sa.sql.expression:
    return sa.select(tags)


def proximity() -> sa.sql.expression:
    return sa.select(
        [tags.c.distance, zones.c.name.label('zone_name'),
         tags.c.name.label('tag_name'), tags.c.type.label('tag_type'),
         tags.c.last_seen, tags.c.id.label('tag_id'), tags.c.zone_id,
         tags.c.alarm_active]).select_from(
        tags.outerjoin(zones)).order_by(tags.c.id.desc())


def get_sensors() -> sa.sql.expression:
    return sa.select(
        [sensors.c.tag_id, sensors.c.type, sensors.c.id,
         sensors.c.ts, sensors.c.value]).order_by(
        sensors.c.tag_id, sensors.c.type, sensors.c.ts.desc()).distinct(
        sensors.c.tag_id, sensors.c.type)


def get_history(tag_id: int):
    return sa.select([history.c.tag_id, history.c.zone_id, history.c.start_ts,
                      history.c.distance, history.c.end_ts,
                      zones.c.name.label('zone_name')]).select_from(
        history.outerjoin(zones)).order_by(
            history.c.start_ts.desc()).where(history.c.tag_id == tag_id)


# def get_contacts(tag_id: int):
#     other_tag_hist = sa.select([
#         history.c.tag_id,
#         history.c.zone_id,
#         history.c.zone_name,
#         history.c.start_ts,
#         tags.c.name.label('tag_name'),
#         sa.func.coalesce(
#             history.c.end_ts,
#             sa.text('(now() at time zone \'utc\')')
#         ).label('end_ts')
#     ]).join(tags, history.c.tag_id == tags.c.id).where(sa.sql.and_(
#         history.c.tag_id != tag_id,
#         tags.c.type.in_(['SmartRelay', 'SecureSmartRelay']))).cte('other')
#     return sa.select([
#         other_tag_hist.c.tag_id,
#         other_tag_hist.c.zone_id,
#         other_tag_hist.c.zone_name.label('zone_name'),
#         other_tag_hist.c.tag_name,
#         sa.func.greatest(
#             history.c.start_ts,
#             other_tag_hist.c.start_ts).label('start_ts'),
#         sa.func.least(
#              history.c.end_ts, other_tag_hist.c.end_ts
#         ).label('end_ts'),
#         sa.func.md5(
#             sa.func.concat(
#                 tag_id,
#                 other_tag_hist.c.tag_id,
#                 other_tag_hist.c.zone_id,
#                 sa.func.greatest(
#                     history.c.start_ts,
#                     other_tag_hist.c.start_ts).label('start_ts'),
#                 sa.func.least(
#                     history.c.end_ts, other_tag_hist.c.end_ts))).label(
#             'hash')
#     ]).select_from(other_tag_hist).join(
#         history, sa.tuple_(history.c.start_ts, history.c.end_ts).op(
#             'overlaps')(sa.tuple_(other_tag_hist.c.start_ts,
#                                   other_tag_hist.c.end_ts))).where(
#         history.c.tag_id == tag_id)

def get_contacts(tag_id: int):
    q = sa.text("""
with target_tag as (
    SELECT tag_id, start_ts, end_ts, zone_id
    from history
    where tag_id = :tag_id
      and tsrange(start_ts, end_ts) && tsrange(:start, :end)
),
     other_tag as (
         SELECT tag_id, start_ts, end_ts, zone_id
         from history
         where tag_id != :tag_id
           and tsrange(start_ts, end_ts) && tsrange(:start, :end)
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
       md5(concat(cast(:tag_id_str as text), tag_id::text, overlap.zone_id,
       start_ts::text,
       end_ts::text)) as hash
from overlap
         join tags on tag_id = tags.id
         join zones on zones.id = overlap.zone_id
         order by start_ts desc limit :limit offset :offset"""  # noqa: E501
                )
    return q.bindparams(tag_id=tag_id, tag_id_str=str(tag_id))


async def get_or_404(db: AsyncConnection,
                     table: sa.Table, t_id: int):
    result = await db.execute(table.select().where(table.c.id == t_id))
    entry = result.first()
    if not entry:
        raise HTTPException(404)
    return entry
