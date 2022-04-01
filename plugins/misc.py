import hikari
import lightbulb

misc = lightbulb.Plugin("Misc")


@misc.command()
@lightbulb.option("text", "Text to repeat", str)
@lightbulb.command("echo", "Repeats user input", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Echo",
        description=f"{ctx.user} said: `{ctx.options.text}`",
        color=0x5865F2,
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(misc)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(misc)
