import os
import datetime

import hikari
import lightbulb


token = os.environ["TOKEN"]
guild_id = os.environ["GUILD_ID"]


class BotApp(lightbulb.BotApp):
    def __init__(self):
        super().__init__(
            token=token,
            default_enabled_guilds=hikari.Snowflake(guild_id),
            help_slash_command=True,
        )
        self.uptime = datetime.datetime.now(datetime.timezone.utc).strftime("%s")


bot = BotApp()

bot.load_extensions_from("./plugins")

bot.run()
