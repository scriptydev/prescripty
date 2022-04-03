import hikari
import lightbulb

import functions


miscellaneous = lightbulb.Plugin("Miscellaneous")


@miscellaneous.command()
@lightbulb.option("text", "Text to repeat", str)
@lightbulb.option("something", "something", str)
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
    bot.add_plugin(miscellaneous)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(miscellaneous)
