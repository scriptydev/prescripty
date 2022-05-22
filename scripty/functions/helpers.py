__all__: list[str] = [
    "datetime_utcnow_aware",
    "get_modules",
    "parse_to_future_datetime",
    "parse_to_timedelta_from_now",
    "validate_time",
]

import asyncio
import datetime
import functools
import pathlib

from types import NoneType
from typing import Generator

import dateparser

from .embed import Embed


def datetime_utcnow_aware() -> datetime.datetime:
    """Helper shorthand for returning now aware utc datetime

    Returns
    -------
    datetime.datetime
        The datetime now returned as utc aware
    """
    return datetime.datetime.now(datetime.timezone.utc)


def get_modules(
    path: str | pathlib.Path,
) -> Generator[pathlib.Path, None, None]:
    """Get the modules from a specified path

    Parameters
    ----------
    path : str | pathlib.Path
        The module to get the path of

    Returns
    -------
    typing.Generator[pathlib.Path, None, None]
        The paths of the modules
    """
    if isinstance(path, str):
        path = pathlib.Path(path)

    return path.rglob("[!_]*.py")


async def parse_to_future_datetime(duration: str) -> datetime.datetime | None:
    """Parse string duration to datetime

    Parameters
    ----------
    duration : str
        The string to parse from

    Returns
    -------
    duration_parsed : datetime.datetime
        The datetime from the input
    None
        If the duration is not parsable or is in the past
    """
    loop = asyncio.get_event_loop()
    duration_parsed = await loop.run_in_executor(
        None,
        functools.partial(
            dateparser.parse,
            date_string=duration,
            settings={  # type: ignore
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "STRICT_PARSING": True,
            },
        ),
    )

    if duration_parsed is None:
        return None

    if duration_parsed < datetime_utcnow_aware():
        return None

    return duration_parsed


async def parse_to_timedelta_from_now(duration: str) -> datetime.timedelta | None:
    """Parse string duration to timedelta from now

    Parameters
    ----------
    duration : str
        The string to parse from

    Returns
    -------
    datetime.timedelta
        The timedelta from now rounded to the nearest second
    None
        If the duration is not parsable or is in the past
    """
    now = datetime_utcnow_aware()

    loop = asyncio.get_event_loop()
    duration_parsed = await loop.run_in_executor(
        None,
        functools.partial(
            dateparser.parse,
            date_string=duration,
            settings={  # type: ignore
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "STRICT_PARSING": True,
            },
        ),
    )

    if duration_parsed is None:
        return None

    if duration_parsed < now:
        return None

    duration_seconds = round(duration_parsed.timestamp() - now.timestamp())
    return datetime.timedelta(seconds=duration_seconds)


def validate_time(
    time: datetime.datetime | datetime.timedelta | None,
    /,
    limit: datetime.timedelta | None = None,
) -> Embed | None:
    """Validate datetime or timedelta

    Parameters
    ----------
    time : datetime.datetime | datetime.timedelta | None
        The time to validate
    limit : datetime.timedelta | None
        The limit to validate against, if any

    Returns
    -------
    Embed
        The hikari error embed to send if the time is invalid
    None
        If the time is valid
    """
    if not isinstance(time, (datetime.datetime, datetime.timedelta, NoneType)):
        raise TypeError(
            f"expected time of datetime.datetime, datetime.timedelta, or None; "
            f"recieved {type(time)}"
        )

    if not isinstance(limit, (datetime.timedelta, NoneType)):
        raise TypeError(f"expected limit of datetime.timedelta; recieved {type(limit)}")

    error = Embed(title="Error")
    error_limit = f"The duration is restricted to the limit of `{limit}`!"

    if time is None:
        error.description = "An exception occurred while parsing specified duration!"
        return error

    if isinstance(time, datetime.datetime):
        if limit is not None and time > datetime_utcnow_aware() + limit:
            error.description = error_limit
            return error

    if isinstance(time, datetime.timedelta):
        if limit is not None and time > limit:
            error.description = error_limit
            return error

    return None
