import hikari
import lightbulb

import functions


misc = lightbulb.Plugin("Miscellaneous")


@misc.command()
@lightbulb.option("text", "Text to repeat", str)
@lightbulb.command("echo", "Repeats user input", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Echo",
        description=f"{ctx.author.mention} said: ```{ctx.options.text}```",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(misc)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(misc)
