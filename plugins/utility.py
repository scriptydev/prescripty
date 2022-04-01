import hikari
import lightbulb


utility = lightbulb.Plugin("Utility")


@utility.command()
@lightbulb.command("ping", "Replies with bot latency", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Ping",
        description=f"Pong! `{round(ctx.app.heartbeat_latency * 1000)}ms`",
        color=0x5865F2,
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(utility)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(utility)
