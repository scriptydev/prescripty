import os

import hikari
import lightbulb


token = os.environ["TOKEN"]
guild_id = os.environ["GUILD_ID"]

bot = lightbulb.BotApp(
    token=token,
    default_enabled_guilds=hikari.Snowflake(guild_id),
    help_slash_command=True,
)

bot.load_extensions_from("./plugins")

bot.run()
