__all__: list[str] = [
    "DISCORD_TOKEN",
    "GUILD_ID_PRIMARY",
    "GUILD_ID_SECONDARY",
    "INVITE_URL",
    "THE_CAT_API_KEY",
]

from typing import Final

import toml

config = toml.load("config.toml")

DISCORD_TOKEN: Final[str] = config["DISCORD_TOKEN"]
GUILD_ID_PRIMARY: Final[int] = config["GUILD_ID_PRIMARY"]
GUILD_ID_SECONDARY: Final[int] = config["GUILD_ID_SECONDARY"]
INVITE_URL: Final[str] = config["INVITE_URL"]
THE_CAT_API_KEY: Final[str] = config["THE_CAT_API_KEY"]
