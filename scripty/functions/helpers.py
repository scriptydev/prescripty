__all__: list[str] = [
    "datetime_now_utc"
    "get_modules",
    "parse_to_future_datetime",
    "parse_to_timedelta_from_now",
]


import asyncio
import datetime
import functools
import pathlib
import typing

import dateparser
import pandas


def datetime_now_utc() -> datetime.datetime:
    """Helper shorthand for returning now aware utc datetime
    
    Returns
    -------
    datetime.datetime
        The datetime now returned as utc aware
    """
    return datetime.datetime.now(datetime.timezone.utc)


def get_modules(
    path: str | pathlib.Path,
) -> typing.Generator[pathlib.Path, None, None]:
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
    parse_duration : datetime.datetime
        The datetime from the input
    None
        If the duration is not parsable or is in the past
    """
    loop = asyncio.get_event_loop()
    parse_duration = await loop.run_in_executor(
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

    if parse_duration is None:
        return None

    if parse_duration < datetime_now_utc():
        return None

    return parse_duration


async def parse_to_timedelta_from_now(
    duration: str,
) -> pandas.Timedelta | None:
    """Parse string duration to timedelta from now

    Parameters
    ----------
    duration : str
        The string to parse from

    Returns
    -------
    pandas.Timedelta
        The timedelta from now rounded to the nearest second
    None
        If the duration is not parsable or is in the past
    """
    now = datetime_now_utc()
    loop = asyncio.get_event_loop()
    parse_duration = await loop.run_in_executor(
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

    if parse_duration is None:
        return None

    if parse_duration < now:
        return None

    calculate_delta = parse_duration - now
    return pandas.to_timedelta(calculate_delta).round("s")  # type: ignore
