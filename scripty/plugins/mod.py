import datetime

import hikari
import lightbulb

from scripty import functions


mod = lightbulb.Plugin("Moderation")


@mod.command()
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)
@lightbulb.option("amount", "Amount to delete", int, min_value=1)
@lightbulb.command("delete", "Purges messages", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def delete(ctx: lightbulb.Context) -> None:
    amount = ctx.options.amount
    channel = ctx.get_channel()

    iterator = ctx.app.rest.fetch_messages(channel).limit(amount)  # .filter()
    async for messages in iterator.chunk(100):
        await ctx.app.rest.delete_messages(channel, messages)

    embed = hikari.Embed(
        title="Delete",
        description=f"`{amount} message(s) deleted",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@delete.set_error_handler()
async def on_delete_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CheckFailure):
        await event.context.respond(f"Missing `MANAGE_MESSAGES` Permission!")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(mod)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(mod)
