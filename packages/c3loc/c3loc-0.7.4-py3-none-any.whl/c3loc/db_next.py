import sqlalchemy as sa  # type: ignore
from sqlalchemy.dialects.postgresql import UUID, MACADDR  # type: ignore

from sqlalchemy.ext.asyncio import (  # type: ignore
    AsyncConnection, create_async_engine)
from .config import DB_URL

engine = create_async_engine(DB_URL, echo=False)
metadata = sa.MetaData()

zones = sa.Table(
    "zones",
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(length=255)),
    sa.Column('attrs', sa.JSON, default='{}'))

groups = sa.Table(
    'groups',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(length=255)),
    sa.Column('attrs', sa.JSON, default='{}'))

alarms = sa.Table(
    'alarms',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('tag_id', sa.ForeignKey('tags.id')),
    sa.Column('start_ts', sa.DateTime,
              default=sa.func.now()),
    sa.Column('last_ts', sa.DateTime,
              default=sa.func.now()),
    sa.Column('ack_ts', sa.DateTime),
    sa.Column('acknowledged', sa.Boolean, default=False),
    sa.Column('priority', sa.Integer, default=0)
)

tags = sa.Table(
    'tags',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(length=255)),
    sa.Column('mac', MACADDR),
    sa.Column('uuid', UUID(as_uuid=True)),
    sa.Column('major', sa.Integer),
    sa.Column('minor', sa.Integer),
    sa.Column('type', sa.Enum(
        'iBeacon', 'SmartRelay', 'LocationAnchor',
        'SecureLocationAnchor', 'SecureSmartRelay', name='tag_type')),
    sa.Column('zone_id', sa.ForeignKey('zones.id')),
    sa.Column('last_seen', sa.DateTime,
              default=sa.func.now()),
    sa.Column('group_id', sa.ForeignKey('groups.id')),
    sa.Column('battery_pct', sa.Integer),
    sa.Column('distance', sa.Numeric(4, 2)),
    sa.Column('bid', sa.BigInteger),
    sa.Column('last_clock', sa.Integer),
    sa.Column('alarm_active', sa.Boolean, default=False),
    sa.Column('zone_start', sa.DateTime,
              default=sa.func.now()),
    sa.Column('attrs', sa.JSON, default={})
)

settings = sa.Table(
    'settings',
    metadata,
    sa.Column('name', sa.String(length=255), nullable=False,
              primary_key=True),
    sa.Column('value', sa.String(length=255), nullable=False),
)

sensors = sa.Table(
    'sensors',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('tag_id', sa.ForeignKey('tags.id'),
              nullable=False),
    sa.Column('type', sa.Integer, nullable=False),
    sa.Column('value', sa.LargeBinary(length=20), nullable=False),
    sa.Column('ts', sa.DateTime,
              default=sa.func.now()),
    sa.Column('device_ts', sa.Integer, nullable=False)
)

log = sa.Table(
    'log',
    metadata,
    sa.Column('tag_id', sa.ForeignKey('tags.id'),
              nullable=False),
    sa.Column('zone_id', sa.ForeignKey('zones.id')),
    sa.Column('ts', sa.DateTime,
              default=sa.func.now()),
    sa.Column('distance', sa.Numeric(4, 2)),
    sa.Column('variance', sa.Float),
    sa.Column('listener_id', sa.ForeignKey('listeners.id')),
    sa.Column('data', sa.JSON, default='{}'),
    sa.Column('anchor_dist', sa.Numeric(4, 2)),
    sa.Column('anchor_ts_delta', sa.Integer),
    sa.Column('anchor_id', sa.ForeignKey('tags.id')),
    sa.Column('reason', sa.Enum('ENTRY', 'MOVE', 'STATUS', 'EXIT',
                                name='report_reason')),
)

listeners = sa.Table(
    'listeners',
    metadata,
    sa.Column('id', sa.String(length=255), primary_key=True),
    sa.Column('name', sa.String(length=255)),
    sa.Column('zone_id', sa.ForeignKey('zones.id')),
    sa.Column('last_seen', sa.DateTime,
              default=sa.func.now()),
    sa.Column('attrs', sa.JSON, default='{}'),
    sa.UniqueConstraint('name', name='listener_name_key')
)

history = sa.Table(
    'history',
    metadata,
    sa.Column('tag_id', sa.ForeignKey('tags.id')),
    sa.Column('zone_id', sa.ForeignKey('zones.id')),
    sa.Column('zone_name', sa.String(length=255)),
    sa.Column('end_ts', sa.DateTime),
    sa.Column('distance', sa.Numeric(4, 2)),
    sa.Column('start_ts', sa.DateTime),
    sa.Column('id', sa.Integer, primary_key=True)
)


async def get_db() -> AsyncConnection:
    conn: AsyncConnection = await engine.connect()
    try:
        yield conn
        await conn.commit()
    except Exception as e:
        await conn.rollback()
        raise e
    finally:
        await conn.close()
