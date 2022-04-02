import hikari
import lightbulb


internal = lightbulb.Plugin("Internal")


@internal.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    embed = hikari.Embed(
        title="Error",
        description="This interaction failed",
        color=0x5865F2,
    )
    await event.context.respond(embed)
    raise exception


def load(bot: lightbulb.BotApp):
    bot.add_plugin(internal)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(internal)
