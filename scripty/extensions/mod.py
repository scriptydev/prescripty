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
@lightbulb.command("delete", "Purge messages", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def delete(ctx: lightbulb.Context) -> None:
    amount = ctx.options.amount
    channel = ctx.get_channel()

    iterator = ctx.app.rest.fetch_messages(channel).limit(amount)  # .filter()
    async for messages in iterator.chunk(100):
        await ctx.app.rest.delete_messages(channel, messages)

    embed = hikari.Embed(
        title="Delete",
        description=f"`{amount}` message(s) deleted",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@delete.set_error_handler()
async def on_delete_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CheckFailure):
        await event.context.respond(f"Missing `MANAGE_MESSAGES` Permission!")


# Setup duration converters later; but for now I want to commit this commented out code
# @mod.command()
# @lightbulb.command("timeout", "Timeout member")
# @lightbulb.implements(lightbulb.SlashCommandGroup)
# async def timeout() -> None:
#     pass


# @timeout.child()
# @lightbulb.add_checks(
#     lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
# )
# @lightbulb.option("reason", "Reason for timeout", str)
# @lightbulb.option("duration", "Duration of the timeout", int)
# @lightbulb.option("member", "Member to timeout", hikari.Member)
# @lightbulb.command("set", "Set timeout for member", auto_defer=True)
# @lightbulb.implements(lightbulb.SlashSubCommand)
# async def set(ctx: lightbulb.Context) -> None:
#     member = ctx.options.member
#     duration = ctx.options.duration

#     await member.edit(communication_disabled_until=duration)

#     embed = hikari.Embed(
#         title="Timeout",
#         description=f"{member.mention} has been timed out for `{duration}` seconds",
#         color=functions.Color.blurple(),
#     )

#     await ctx.respond(embed)


# @timeout.child()
# @lightbulb.add_checks(
#     lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
# )
# @lightbulb.option("member", "Member to timeout", hikari.Member)
# @lightbulb.command("remove", "Remove timeout from member", auto_defer=True)
# @lightbulb.implements(lightbulb.SlashSubCommand)
# async def remove(ctx: lightbulb.Context) -> None:
#     member = ctx.options.member

#     await member.edit(communication_disabled_until=None)

#     embed = hikari.Embed(
#         title="Timeout",
#         description=f"{member.mention} has been removed from timeout",
#         color=functions.Color.blurple(),
#     )

#     await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(mod)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(mod)