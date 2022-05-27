from __future__ import annotations

__all__: tuple[str, ...] = (
    "datetime_utcnow_aware",
    "discord_timestamp",
    "generate_oauth",
    "get_modules",
    "parse_to_future_datetime",
    "parse_to_timedelta_from_now",
    "validate_and_encode_url",
)

import asyncio
import datetime
import functools
import pathlib
import re
import urllib.parse

from typing import Generator, Iterable, Literal

import hikari
import dateparser


def datetime_utcnow_aware() -> datetime.datetime:
    """Helper shorthand for returning now aware utc datetime

    Returns
    -------
    datetime.datetime
        The datetime now returned as utc aware
    """
    return datetime.datetime.now(datetime.timezone.utc)


TimestampStyle = Literal["t", "T", "d", "D", "f", "F", "R"]


# Adapted from discord.py utils for hikari
def discord_timestamp(
    timestamp: datetime.datetime,
    /,
    style: TimestampStyle = "f",
) -> str:
    """Convert a datetime to a Discord timestamp

    Parameters
    ----------
    datetime : datetime.datetime
        The timestamp or datetime to convert
    style : TimestampStyle
        The style of the timestamp, defaults to Literal["f"]

    Returns
    -------
    str
        The Discord timestamp representation
    """
    return f"<t:{int(timestamp.timestamp())}:{style}>"


# Adapted from discord.py utils for hikari
def generate_oauth(
    client_id: int | str,
    *,
    permissions: hikari.UndefinedOr[hikari.Permissions] = hikari.UNDEFINED,
    guild: hikari.UndefinedOr[hikari.Snowflake] = hikari.UNDEFINED,
    redirect_uri: hikari.UndefinedOr[str] = hikari.UNDEFINED,
    scopes: hikari.UndefinedOr[Iterable[str]] = hikari.UNDEFINED,
    disable_guild_select: hikari.UndefinedOr[bool] = hikari.UNDEFINED,
) -> str:
    """A helper function that returns the OAuth2 URL for inviting the bot
    into guilds

    Parameters
    -----------
    client_id: int | str
        The client ID for your bot
    permissions: hikari.UndefinedOr[hikari.Snowflake]
        Optional permissions to invite the bot with
    guild: hikari.UndefinedOr[hikari.Snowflake]
        The guild to pre-select in the authorization screen, if available
    redirect_uri: hikari.UndefinedOr[str]
        An optional valid redirect URI
    scopes: hikari.UndefinedOr[Iterable[str]]
        An optional valid list of scopes. Defaults to ``('bot', 'applications.commands')``
    disable_guild_select: hikari.UndefinedOr[bool]
        Whether to disallow the user from changing the guild dropdown

    Returns
    --------
    str
        The OAuth2 URL for inviting the bot into guilds
    """
    url = f"https://discord.com/oauth2/authorize?client_id={client_id}"
    url += "&scope=" + "+".join(scopes or ("bot", "applications.commands"))

    if permissions is not hikari.UNDEFINED:
        url += f"&permissions={permissions.value}"

    if guild is not hikari.UNDEFINED:
        url += f"&guild_id={guild}"

    if redirect_uri is not hikari.UNDEFINED:
        url += "&response_type=code&" + urllib.parse.urlencode(
            {"redirect_uri": redirect_uri}
        )

    if disable_guild_select is not hikari.UNDEFINED:
        url += "&disable_guild_select=true"

    return url


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

    if duration_parsed is None or duration_parsed < datetime_utcnow_aware():
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

    if duration_parsed is None or duration_parsed < now:
        return None

    duration_seconds = round(duration_parsed.timestamp() - now.timestamp())
    return datetime.timedelta(seconds=duration_seconds)


def validate_and_encode_url(url: str) -> dict[str, str] | None:
    """Validate and encode a specifed url

    Parameters
    ----------
    url : str
        The url to validate and/or encode

    Returns
    -------
    str | None
        Returns the encoded url if valid, otherwise None
    """
    url_primary_regex = re.compile(
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    url_primary_search = re.search(url_primary_regex, url)

    if url_primary_search is None:
        return None

    url_http_regex = re.compile(r"^(?:http|ftp)s?://")
    url_http_match = re.match(url_http_regex, url)

    if url_http_match is None:
        url = f"https://{url}"

    return {"input": url, "encoded": urllib.parse.quote_plus(url)}
