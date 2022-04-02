import hikari
import lightbulb


miscellaneous = lightbulb.Plugin("Miscellaneous")


@miscellaneous.command()
@lightbulb.option("text", "Text to repeat", str)
@lightbulb.command("echo", "Repeats user input", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Echo",
        description=f"{ctx.author.mention} \n\n`{ctx.options.text}`",
        color=0x5865F2,
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(miscellaneous)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(miscellaneous)
