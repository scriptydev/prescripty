import toml


__all__: list[str] = [
    "DISCORD_TOKEN",
    "GUILD_ID_PRIMARY",
    "GUILD_ID_SECONDARY",
    "INVITE_URL",
]

config = toml.load("config.toml")

DISCORD_TOKEN: str = config["discord_token"]
GUILD_ID_PRIMARY: int = config["guild_id_primary"]
GUILD_ID_SECONDARY: int = config["guild_id_secondary"]
INVITE_URL: str = config["invite_url"]
