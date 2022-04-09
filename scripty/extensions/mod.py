import asyncio
import concurrent
import datetime

import dateparser
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

    iterator = (
        ctx.app.rest.fetch_messages(channel).limit(amount)
        # .filter(...)
    )
    tasks = []
    async for messages in iterator.chunk(100):
        task = asyncio.create_task(ctx.app.rest.delete_messages(channel, messages))
        tasks.append(task)

    def generate_embed(message: str) -> hikari.Embed:
        return hikari.Embed(
            title="Delete",
            description=message,
            color=functions.Color.green(),
        )

    if tasks:
        await asyncio.wait(tasks)

        if amount == 1:
            await ctx.respond(generate_embed(f"`{amount} message` deleted"))

        else:
            await ctx.respond(generate_embed(f"`{amount} messages` deleted"))

    else:
        embed = hikari.Embed(
            title="Delete Error",
            description="No messages to delete!",
            color=functions.Color.red(),
        )
        await ctx.respond(embed)


@delete.set_error_handler()
async def on_delete_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CheckFailure):
        embed = hikari.Embed(
            title="Delete Error",
            description="Missing `MANAGE_MESSAGES` permission!",
            color=functions.Color.red(),
        )
        await event.context.respond(embed)


# This command still needs major work. The basic functionality is there, however parsing durations using the dateparser library is still a bit of a mess with blocking asyncio. Our idea solution might be to create out custom parser instead. We also need to add error handling later.
@mod.command()
@lightbulb.command("timeout", "Timeout member", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def timeout() -> None:
    pass


@timeout.child()
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)
@lightbulb.option("reason", "Reason for timeout", str, required=False)
@lightbulb.option("duration", "Duration of the timeout", str)
@lightbulb.option("member", "Member to timeout", hikari.Member)
@lightbulb.command("set", "Set timeout for member", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set(ctx: lightbulb.Context) -> None:
    member = ctx.options.member
    duration = ctx.options.duration
    reason = ctx.options.reason or None

    def get_duration(duration) -> datetime.datetime or None:
        duration = dateparser.parse(duration, settings={"PREFER_DATES_FROM": "future"})
        return duration

    async def async_duration(loop, executor):
        await asyncio.wait(
            fs={loop.run_in_executor(executor, get_duration, duration)},
            return_when=asyncio.ALL_COMPLETED,
        )

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor()
    duration = await loop.create_task(async_duration(loop, executor))

    if not duration:
        await ctx.respond("Invalid duration!")

    else:
        duration_resolved = int(round(duration.timestamp()))
        duration_resolved_full = f"<t:{duration_resolved}:F>"
        duration_resolved_relative = f"<t:{duration_resolved}:R>"

        await member.edit(communication_disabled_until=duration)

        embed = hikari.Embed(
            title="Timeout",
            description=f"Timed out **{str(member)}** until {duration_resolved_full} {duration_resolved_relative} \nReason: `{reason}`",
            color=functions.Color.green(),
        )

        await ctx.respond(embed)


@timeout.child()
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)
@lightbulb.option("member", "Member to timeout", hikari.Member)
@lightbulb.command("remove", "Remove timeout from member", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.Context) -> None:
    member = ctx.options.member

    if not member.communication_disabled_until:
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
