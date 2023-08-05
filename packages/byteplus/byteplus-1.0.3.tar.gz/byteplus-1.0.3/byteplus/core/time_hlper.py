from datetime import timedelta, datetime, timezone


def rfc3339_format(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def milliseconds(delta: timedelta) -> int:
    return int(delta.total_seconds() * 1000.0)
