__all__: list[str] = [
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
    parse_duration : datetime.datetime | None
        The datetime from the input
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

    if parse_duration < datetime.datetime.now(datetime.timezone.utc):
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
    timedelta : pandas.Timedelta | None
        The timedelta from now rounded to the nearest second
    None
    """
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
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

    if parse_duration < datetime.datetime.now(datetime.timezone.utc):
        return None

    calculate_delta = parse_duration - datetime_now
    return pandas.to_timedelta(calculate_delta).round("s")  # type: ignore
