import os
from datetime import datetime
from typing import Union

import pytz

TzInfoType = Union[type(pytz.UTC), pytz.tzinfo.DstTzInfo]
StrTzInfoType = Union[TzInfoType, str]


def get_current_timezone() -> TzInfoType:
    return pytz.timezone(os.environ["TZ"])


def get_current_timezone_name() -> str:
    return get_current_timezone().tzname(None)


def now() -> datetime:
    return datetime.now(get_current_timezone())


def is_aware(value: datetime) -> bool:
    return value.utcoffset() is not None


def is_naive(value: datetime) -> bool:
    return value.utcoffset() is None


def make_aware(
        value: datetime,
        timezone: StrTzInfoType = None,
        is_dst: bool = False,
) -> datetime:
    assert is_naive(value), "expects a naive datetime"

    if timezone is None:
        timezone = get_current_timezone()
    elif isinstance(timezone, str):
        timezone = pytz.timezone(timezone)
    else:
        pass

    return timezone.localize(value, is_dst=is_dst)


def make_naive(
        value: datetime,
        timezone: StrTzInfoType = None,
) -> datetime:
    assert is_aware(value), "expects an aware datetime"

    if timezone is None:
        timezone = get_current_timezone()
    elif isinstance(timezone, str):
        timezone = pytz.timezone(timezone)
    else:
        pass

    return value.astimezone(timezone).replace(tzinfo=None)


def get_beginning_datetime(
        *,
        year: int,
        month: int = 1,
        day: int = 1,
        timezone: StrTzInfoType = None,
        is_dst: bool = False,
) -> datetime:
    _datetime = datetime(year, month, day)
    return make_aware(_datetime, timezone=timezone, is_dst=is_dst)
