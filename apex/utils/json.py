from datetime import datetime
from zoneinfo import ZoneInfo

import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes,
    # to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


json_loads = orjson.loads
json_dumps = orjson_dumps
