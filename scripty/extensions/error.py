import hikari
import lightbulb

from scripty import functions


error = lightbulb.Plugin("Error")


@error.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        embed = hikari.Embed(
            title="Error",
            description="This interaction failed!",
            color=functions.Color.red(),
        )
        await event.context.respond(embed)
        raise event.exception


def load(bot: lightbulb.BotApp):
    bot.add_plugin(error)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(error)
