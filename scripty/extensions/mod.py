import asyncio
import datetime

import dateparser
import hikari
import lightbulb

from scripty import functions


mod = lightbulb.Plugin("Moderation")


@mod.command()
@lightbulb.add_checks(
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
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


@mod.command()
@lightbulb.command("timeout", "Timeout member", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def timeout() -> None:
    pass


@timeout.child()
@lightbulb.add_checks(
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS),
    lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS),
)
@lightbulb.option("reason", "Reason for timeout", str, required=False)
@lightbulb.option("duration", "Duration of the timeout", str)
@lightbulb.option("member", "Member to timeout", hikari.Member)
@lightbulb.command("set", "Set timeout for member", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set(ctx: lightbulb.Context) -> None:
    member = ctx.options.member
    duration = ctx.options.duration
    reason = ctx.options.reason or hikari.UNDEFINED

    def parse_duration(duration) -> datetime.datetime or None:
        return dateparser.parse(
            duration,
            settings={"PREFER_DATES_FROM": "future", "RETURN_AS_TIMEZONE_AWARE": True},
        )

    loop = asyncio.get_event_loop()

    duration = await loop.run_in_executor(None, parse_duration, duration)

    timeout_limit = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=28
    )

    if not duration:
        embed = hikari.Embed(
            title="Timeout Error",
            description="Invalid duration provided!",
            color=functions.Color.red(),
        )
        await ctx.respond(embed)

    elif duration < datetime.datetime.now(datetime.timezone.utc):
        embed = hikari.Embed(
            title="Timeout Error",
            description="Duration must be in the future!",
            color=functions.Color.red(),
        )
        await ctx.respond(embed)

    elif duration > timeout_limit:
        embed = hikari.Embed(
            title="Timeout Error",
            description="Duration cannot be longer than `28 days`!",
            color=functions.Color.red(),
        )
        await ctx.respond(embed)

    else:
        duration_resolved = int(round(duration.timestamp()))
        duration_resolved_full = f"<t:{duration_resolved}:F>"

        await member.edit(communication_disabled_until=duration)

        embed = hikari.Embed(
            title="Timeout",
            description=f"Timed out **{str(member)}** until {duration_resolved_full} \nReason: `{'No reason provided' if reason is hikari.UNDEFINED else reason}`",
            color=functions.Color.green(),
        )

        await ctx.respond(embed)


@set.set_error_handler()
async def on_set_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, hikari.BadRequestError):
        embed = hikari.Embed(
            title="Timeout Error",
            description="Invalid duration provided!",
            color=functions.Color.red(),
        )
        await event.context.respond(embed)


@timeout.child()
@lightbulb.add_checks(
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS),
    lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS),
)
@lightbulb.option("member", "Member to timeout", hikari.Member)
@lightbulb.command("remove", "Remove timeout from member", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.Context) -> None:
    member: hikari.Member = ctx.options.member

    if not member.communication_disabled_until():
        embed = hikari.Embed(
            title="Timeout Error",
            description="You cannot remove timeout from member that is not timed out!",
            color=functions.Color.red(),
        )
        await ctx.respond(embed)

    else:
        await member.edit(communication_disabled_until=None)

        embed = hikari.Embed(
            title="Timeout",
            description=f"Removed timeout from **{str(member)}**",
            color=functions.Color.green(),
        )

        await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(mod)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(mod)
