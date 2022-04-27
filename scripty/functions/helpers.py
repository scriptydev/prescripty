__all__: list[str] = ["get_modules", "parse_duration"]


import asyncio
import datetime
import functools
import pathlib
import typing

import dateparser


def get_modules(
    path: str | pathlib.Path,
) -> typing.Generator[pathlib.Path, None, None]:
    """Get the modules from a specified path

    Parameters
    ----------
    path : str | Path
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


async def parse_duration(duration: str) -> datetime.datetime | None:
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

    return parse_run
