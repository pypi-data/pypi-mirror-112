from binascii import unhexlify
import os
from typing import Dict, Union
from uuid import UUID

CONFIG: Dict[str, Union[str, int, UUID, bytes]] = {
    'DB_NAME': os.getenv('DB_NAME', ''),
    'DB_USER': os.getenv('DB_USER', 'c3loc'),
    'DB_PASSWORD': os.getenv('DB_PASSWORD', 'c3letmein'),
    'DB_HOST': os.getenv('DB_HOST', ''),
    'LA_UUID': os.getenv('LA_UUID', UUID(bytes=b'c3wirelesslocanc')),
    'API_RESULT_LIMIT': int(os.getenv('API_RESULT_LIMIT', 100)),
    'API_RESULT_LIMIT_CONTACTS':
        int(os.getenv('API_RESULT_LIMIT_CONTACTS', 5000)),
    'LOCATION_UPDATE_MS': 1000,
    'MAX_FRAME_SIZE': int(os.getenv('MAX_FRAME_SIZE', 5 * 1024 * 1024)),
    'SSR_KEY': unhexlify(os.getenv('SSR_KEY', b'c3wirelesslocanc'.hex())),
    'STATS_INTERVAL': int(os.getenv('STATS_INTERVAL', 60)),
    'MAX_DB_CONNECTIONS': int(os.getenv('MAX_DB_CONNECTIONS', 4)),
    'MAX_QUEUED_PACKETS': int(os.getenv('MAX_QUEUED_PACKETS', 100)),
    'LAST_SEEN_RESOLUTION_SECS':
        int(os.getenv('LAST_SEEN_RESOLUTION_SECS', 5)),
    'MIN_SEC_IN_LOCATION': int(os.getenv('MIN_SEC_IN_LOCATION', 10)),
    'MIN_SEC_IN_LOCATION_IF_RETURNING':
        int(os.getenv('MIN_SEC_IN_LOCATION_IF_RETURNING', 30)),
}

DB_RELEVANT = {
    'ingest': {'MIN_SEC_IN_LOCATION': CONFIG['MIN_SEC_IN_LOCATION'],
               'MIN_SEC_IN_LOCATION_IF_RETURNING':
                   CONFIG['MIN_SEC_IN_LOCATION_IF_RETURNING']},
    'api': {}
}

DB_PATH = os.getenv(
    'DB_PATH',
    f'{CONFIG["DB_USER"]}:{CONFIG["DB_PASSWORD"]}'  # type: ignore
    f'@{CONFIG["DB_HOST"]}/{CONFIG["DB_NAME"]}')

DB_URL = os.getenv(
    'DB_URL',
    f'postgresql+asyncpg://{DB_PATH}')  # type: ignore
