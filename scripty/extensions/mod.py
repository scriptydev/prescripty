import asyncio
import datetime

import dateparser
import hikari
import lightbulb

from scripty import functions


mod = lightbulb.Plugin("Moderation")


@mod.command()
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("reason", "Reason for ban", str, required=False)
@lightbulb.option(
    "delete_message_days",
    "Days to delete user messages",
    int,
    required=False,
    min_value=1,
    max_value=7,
)
@lightbulb.option("user", "User to ban", hikari.User)
@lightbulb.command("ban", "Ban user from server", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ban(ctx: lightbulb.Context) -> None:
    user = ctx.options.user
    delete_message_days = ctx.options.delete_message_days or hikari.UNDEFINED
    reason = ctx.options.reason or hikari.UNDEFINED
    guild = ctx.guild_id

    await ctx.app.rest.ban_user(
        guild, user, delete_message_days=delete_message_days, reason=reason
    )

    embed = hikari.Embed(
        title="Ban",
        description=f"Banned **{str(user)}** \nReason: `{'No reason provided' if reason is hikari.UNDEFINED else reason}`",
        color=functions.Color.green(),
    )

    await ctx.respond(embed)


@ban.set_error_handler()
async def on_ban_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CheckFailure):
        embed = hikari.Embed(
            title="Ban Error",
            description="`BAN_MEMBERS` permission missing!",
            color=functions.Color.red(),
        )
        await event.context.respond(embed)


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
    channel = ctx.channel_id

    bulk_delete_limit = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(days=14)

    iterator = (
        ctx.app.rest.fetch_messages(channel)
        .take_while(lambda message: message.created_at > bulk_delete_limit)
        .limit(amount)
    )

    count = 0
    tasks = []
    async for messages in iterator.chunk(100):
        count += len(messages)
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

        if count < amount:
            if count == 1:
                await ctx.respond(
                    generate_embed(
                        f"`{count} message` deleted \nOlder messages past `14 days` cannot be deleted"
                    )
                )

            else:
                await ctx.respond(
                    generate_embed(
                        f"`{count} messages` deleted \nOlder messages past `14 days` cannot be deleted"
                    )
                )

        elif count == 1:
            await ctx.respond(generate_embed(f"`{count} message` deleted"))

        else:
            await ctx.respond(generate_embed(f"`{count} messages` deleted"))

    else:
        embed = hikari.Embed(
            title="Delete Error",
            description="Unable to delete messages! \nMessages are older than `14 days` or do not exist",
            color=functions.Color.red(),
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
