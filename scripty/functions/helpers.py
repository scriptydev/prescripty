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
    modules : typing.Generator[Path, None, None]
        The paths of the modules
    """
    if isinstance(path, str):
        path = pathlib.Path(path)

    modules = path.rglob("[!_]*.py")

    return modules


async def parse_to_datetime(duration: str) -> datetime.datetime | None:
    loop = asyncio.get_event_loop()

    parse_run = await loop.run_in_executor(
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

    if parse_run is None:
        raise ValueError("could not parse to datetime from input")

    return parse_run


async def parse_to_timedelta_from_now(
    duration: str,
) -> datetime.timedelta | None:
    loop = asyncio.get_event_loop()

    parse_run = await loop.run_in_executor(
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

    if parse_run is None:
        raise ValueError("could not parse to datetime from input")

    timedelta_from_now = parse_run - datetime.datetime.now(
        datetime.timezone.utc
    )

    timedelta_round = pandas.to_timedelta(timedelta_from_now).round("s")  # type: ignore

    return timedelta_round
