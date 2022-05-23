from __future__ import annotations

__all__: Sequence[str] = (
    "DISCORD_TOKEN",
    "GUILD_ID_PRIMARY",
    "GUILD_ID_SECONDARY",
    "INVITE_URL",
    "THE_CAT_API_KEY",
)

from typing import Final, Sequence

import toml

# Try to load the private config file and catch FileNotFoundError
# to instead load a sample file. This avoids the error when running
# unittest continuous integration checks.
try:
    config = toml.load("_config.toml")
except FileNotFoundError:
    config = toml.load("config.toml")

DISCORD_TOKEN: Final[str] = config["DISCORD_TOKEN"]
GUILD_ID_PRIMARY: Final[int] = config["GUILD_ID_PRIMARY"]
GUILD_ID_SECONDARY: Final[int] = config["GUILD_ID_SECONDARY"]
INVITE_URL: Final[str] = config["INVITE_URL"]
THE_CAT_API_KEY: Final[str] = config["THE_CAT_API_KEY"]
