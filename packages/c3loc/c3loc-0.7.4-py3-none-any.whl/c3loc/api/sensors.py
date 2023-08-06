import enum
from functools import partial

import pytz
from aiohttp import web
from aiohttp_cors import CorsViewMixin  # type: ignore

from .views import paginate_query


class SensorType(enum.IntEnum):
    Battery = 0
    Temperature = 1
    Humidity = 2


API_SENSOR_NAME_MAP = {
    SensorType.Battery: "SensorDataBattery",
    SensorType.Temperature: "SensorDataTemp",
    SensorType.Humidity: "SensorDataHumid",
}


def fixed_point(divisor, data, signed=True):
    val = int.from_bytes(data, 'little', signed=signed)
    return val / divisor


def percent_formatter(data):
    return int.from_bytes(data, 'little', signed=False)


def format_sensor(tag, data):
    dispatch = {SensorType.Battery: percent_formatter,
                SensorType.Temperature: partial(fixed_point, 10),
                SensorType.Humidity: percent_formatter}
    if tag not in dispatch:
        return None
    return dispatch[tag](data)


def format_sensors(sensors):
    out = []
    for sensor in sensors:
        ts = sensor['ts']
        value = format_sensor(sensor['type'], sensor['value'])
        if value is None:
            continue
        out.append({
            "sensor_type": API_SENSOR_NAME_MAP[sensor['type']],
            "ts": ts.replace(tzinfo=pytz.utc).isoformat(),
            "value": value
        })
    return out


SENSORS_QUERY = """SELECT * from (
SELECT DISTINCT ON (tag_id, type) *
FROM sensors
ORDER BY tag_id, type, ts DESC) as filter
"""


class SensorsView(web.View, CorsViewMixin):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = (SENSORS_QUERY,)
            query = paginate_query(self.request, query)
            sensors = await conn.fetch(*query)
            out = []
            for sensor in sensors:
                ts = sensor['ts']
                value = format_sensor(sensor['type'], sensor['value'])
                if value is None:
                    continue
                out.append({
                    "tag_id": sensor['tag_id'],
                    "sensor_type": API_SENSOR_NAME_MAP[sensor['type']],
                    "ts": ts.replace(tzinfo=pytz.utc).isoformat(),
                    "value": value
                })
            return web.json_response(out)


__all__ = ['API_SENSOR_NAME_MAP', 'format_sensors', 'SensorType',
           'SensorsView']
