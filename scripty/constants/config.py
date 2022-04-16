import os

# Strange type issue with dotenv
from dotenv import load_dotenv

import hikari


load_dotenv()

DEV_ID: hikari.Snowflake = hikari.Snowflake(os.environ["GUILD_ID_PRIMARY"])
GUILD_IDS: tuple[hikari.Snowflake, ...] = (
    hikari.Snowflake(os.environ["GUILD_ID_PRIMARY"]),
    hikari.Snowflake(os.environ["GUILD_ID_SECONDARY"]),
)
INVITE_URL: str = os.environ["INVITE_URL"]
TOKEN: str = os.environ["TOKEN"]
