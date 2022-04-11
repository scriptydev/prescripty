import os
from dotenv import load_dotenv

import hikari


load_dotenv()


TOKEN: str = os.environ["TOKEN"]

GUILD_IDS: tuple[hikari.Snowflake, ...] = (
    hikari.Snowflake(os.environ["GUILD_ID_PRIMARY"]),
    hikari.Snowflake(os.environ["GUILD_ID_SECONDARY"]),
)

INVITE_URL: str = "https://discord.com/api/oauth2/authorize?client_id=883496337616822302&permissions=8&scope=bot%20applications.commands"
