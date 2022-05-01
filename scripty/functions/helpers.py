__all__: list[str] = [
    "get_modules",
    "parse_to_datetime",
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
    modules : typing.Generator[pathlib.Path, None, None]
        The paths of the modules
    """
    if isinstance(path, str):
        path = pathlib.Path(path)

    modules = path.rglob("[!_]*.py")

    return modules


async def parse_to_datetime(duration: str) -> datetime.datetime | None:
    """Parse string duration to datetime

    Parameters
    ----------
    duration : str
        The string to parse from

    Returns
    -------
    parse : datetime.datetime | None
        The datetime from the input
    """
    loop = asyncio.get_event_loop()

    parse = await loop.run_in_executor(
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

    if parse is None:
        return

    return parse


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
    loop = asyncio.get_event_loop()

    parse = await loop.run_in_executor(
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

    if parse is None:
        return

    timedelta_calc = parse - datetime.datetime.now(datetime.timezone.utc)
    timedelta: pandas.Timedelta = pandas.to_timedelta(timedelta_calc).round("s")  # type: ignore

    return timedelta
