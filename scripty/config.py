__all__: list[str] = [
    "DISCORD_TOKEN",
    "GUILD_ID_PRIMARY",
    "GUILD_ID_SECONDARY",
    "INVITE_URL",
    "THE_CAT_API_KEY",
]

import typing

import toml

config = toml.load("config.toml")

DISCORD_TOKEN: typing.Final[str] = config["DISCORD_TOKEN"]
GUILD_ID_PRIMARY: typing.Final[int] = config["GUILD_ID_PRIMARY"]
GUILD_ID_SECONDARY: typing.Final[int] = config["GUILD_ID_SECONDARY"]
INVITE_URL: typing.Final[str] = config["INVITE_URL"]
THE_CAT_API_KEY: typing.Final[str] = config["THE_CAT_API_KEY"]
