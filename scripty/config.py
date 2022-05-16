__all__: list[str] = [
    "AERO_API_KEY",
    "CLIENT_ID"
    "DISCORD_TOKEN",
    "GUILD_ID_PRIMARY",
    "GUILD_ID_SECONDARY",
    "THE_CAT_API_KEY",
]

from typing import Final

import toml

# Try to load the private config file and catch FileNotFoundError
# to instead load a sample file. This avoids the error when running
# unittest continuous integration checks.
try:
    config = toml.load("_config.toml")
except FileNotFoundError:
    config = toml.load("config.toml")

AERO_API_KEY: Final[str] = config["AERO_API_KEY"]
CLIENT_ID: Final[int] = config["CLIENT_ID"]
DISCORD_TOKEN: Final[str] = config["DISCORD_TOKEN"]
GUILD_ID_PRIMARY: Final[int] = config["GUILD_ID_PRIMARY"]
GUILD_ID_SECONDARY: Final[int] = config["GUILD_ID_SECONDARY"]
THE_CAT_API_KEY: Final[str] = config["THE_CAT_API_KEY"]
