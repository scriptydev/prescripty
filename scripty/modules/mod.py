import asyncio
import datetime
import functools
import typing

import hikari
import tanchi
import tanjun

import scripty


component = tanjun.Component()


@component.with_command
@tanjun.with_own_permission_check(hikari.Permissions.BAN_MEMBERS)
@tanjun.with_author_permission_check(hikari.Permissions.BAN_MEMBERS)
@tanchi.as_slash_command()
async def ban(
    ctx: tanjun.abc.SlashContext,
    user: hikari.User,
    delete_message_days: hikari.UndefinedNoneOr[tanchi.Range[1, 7]] = None,
    reason: hikari.UndefinedNoneOr[str] = None,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Ban user from server

    Parameters
    ----------
    user : hikari.User
        User to ban
    delete_message_days : hikari.UndefinedNoneOr[tanchi.Range[int, int]]
        Days to delete user messages
    reason : hikari.UndefinedNoneOr[str]
        Reason for ban
    """
    delete_message_days = delete_message_days or hikari.UNDEFINED
    reason = reason or hikari.UNDEFINED
    guild = ctx.guild_id

    if guild is None:
        await ctx.respond(
            scripty.Embed(
                title="Ban Error",
                description="This command must be invoked in a guild!",
            )
        )
        return

    await bot.rest.ban_user(
        guild, user, delete_message_days=delete_message_days, reason=reason
    )

    await ctx.respond(
        scripty.Embed(
            title="Ban",
            description=f"Banned **{str(user)}**\nReason: `{reason or 'No reason provided'}`",
        )
    )


@component.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MANAGE_MESSAGES)
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_MESSAGES)
@tanchi.as_slash_command(default_to_ephemeral=True)
async def delete(
    ctx: tanjun.abc.SlashContext,
    amount: tanchi.Range[1, ...],
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Purge messages from channel

    Parameters
    ----------
    amount : tanchi.Range[int, ...]
        Amount to delete
    """
    channel = ctx.channel_id

    bulk_delete_limit = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(days=14)

    iterator = (
        bot.rest.fetch_messages(channel)
        .take_while(lambda message: message.created_at > bulk_delete_limit)
        .limit(amount)
    )

    count = 0
    tasks: typing.Any | None = []
    async for messages in iterator.chunk(100):
        count += len(messages)
        task = asyncio.create_task(bot.rest.delete_messages(channel, messages))
        tasks.append(task)

    def generate_embed(message: str) -> scripty.Embed:
        return scripty.Embed(
            title="Delete",
            description=message,
        )

    if tasks:
        await asyncio.wait(tasks)

        if count < amount:
            if count == 1:
                await ctx.respond(
                    generate_embed(
                        f"`{count} message` deleted\nOlder messages past `14 days` cannot be deleted"
                    )
                )
                return

            await ctx.respond(
                generate_embed(
                    f"`{count} messages` deleted\nOlder messages past `14 days` cannot be deleted"
                )
            )

        if count == 1:
            await ctx.respond(generate_embed(f"`{count} message` deleted"))
            return

        await ctx.respond(generate_embed(f"`{count} messages` deleted"))
        return

    embed = scripty.Embed(
        title="Delete Error",
        description=(
            "Unable to delete messages!\n"
            "Messages are older than `14 days` or do not exist"
        ),
    )
    await ctx.respond(embed)


@component.with_command
@tanjun.with_own_permission_check(hikari.Permissions.KICK_MEMBERS)
@tanjun.with_author_permission_check(hikari.Permissions.KICK_MEMBERS)
@tanchi.as_slash_command()
async def kick(
    ctx: tanjun.abc.SlashContext,
    member: hikari.Member,
    reason: hikari.UndefinedNoneOr[str] = None,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Kick member from server

    Parameters
    ----------
    member : hikari.Member
        Member to kick
    reason : hikari.UndefinedNoneOr[str]
        Reason for kick
    """
    reason = reason or hikari.UNDEFINED
    guild = ctx.guild_id

    if guild is None:
        await ctx.respond(
            scripty.Embed(
                title="Kick Error",
                description="This command must be invoked in a guild!",
            )
        )
        return

    await bot.rest.kick_user(guild, member)
    await ctx.respond(
        scripty.Embed(
            title="Kick",
            description=(
                f"Kicked **{str(member)}**\n"
                f"Reason: `{reason or 'No reason provided'}`"
            ),
        )
    )


slowmode = component.with_slash_command(
    tanjun.slash_command_group("slowmode", "Slowmode channel")
)


@slowmode.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanchi.as_slash_command("enable")
async def slowmode_enable(
    ctx: tanjun.abc.SlashContext,
    duration: tanchi.Converted[datetime.timedelta, scripty.parse_to_timedelta_from_now],
    channel: hikari.TextableGuildChannel | None = None,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Enable slowmode for channel

    Parameters
    ----------
    channel : hikari.TextableGuildChannel
        Channel to enable slowmode
    duration : tanchi.Converted[
        datetime.timedelta, scripty.parse_to_timedelta_from_now
    ]
        Duration of slowmode
    """
    channel = channel or ctx.get_channel()
    duration_limit = datetime.timedelta(hours=6)
    error = scripty.Embed(
        title="Slowmode Error",
    )

    if channel is None:
        error.description = "This command must be invoked in a guild!"
        await ctx.respond(error)
        return
    if duration is None:
        error.description = "Unable to parse specified duration; invalid time!"
        await ctx.respond(error)
        return
    if duration > duration_limit:
        error.description = "Duration cannot be greater than `6 hours!`"
        await ctx.respond(error)
        return

    await bot.rest.edit_channel(channel, rate_limit_per_user=duration)
    await ctx.respond(
        scripty.Embed(
            title="Slowmode",
            description=f"Enabled slowmode for **{str(channel)}** to `{duration}s`",
        )
    )


@slowmode.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanchi.as_slash_command("disable")
async def slowmode_disable(
    ctx: tanjun.abc.SlashContext,
    channel: hikari.TextableGuildChannel | None = None,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Disable slowmode from channel

    Parameters
    ----------
    channel : hikari.TextableGuildChannel
        Channel to disable slowmode
    """
    channel = channel or ctx.get_channel()

    if channel is None:
        await ctx.respond(
            scripty.Embed(
                title="Slowmode Error",
                description="This command must be invoked in a guild!",
            )
        )
        return

    await bot.rest.edit_channel(channel, rate_limit_per_user=0)
    await ctx.respond(
        scripty.Embed(
            title="Slowmode",
            description=f"Removed slowmode from **{str(channel)}**",
        )
    )


timeout = component.with_slash_command(
    tanjun.slash_command_group("timeout", "Timeout member")
)


@timeout.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MODERATE_MEMBERS)
@tanjun.with_author_permission_check(hikari.Permissions.MODERATE_MEMBERS)
@tanchi.as_slash_command("set")
async def timeout_set(
    ctx: tanjun.abc.SlashContext,
    member: hikari.Member,
    duration: tanchi.Converted[datetime.datetime, scripty.parse_to_future_datetime],
    reason: hikari.UndefinedNoneOr[str] = None,
) -> None:
    """Set timeout for member

    Parameters
    ----------
    member : hikari.Member
        Member to timeout
    duration : tanchi.Converted[datetime.datetime, scripty.parse_duration]
        Duration of the timeout
    reason : hikari.UndefinedNoneOr[str]
        Reason for timeout
    """
    timeout_limit = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=28
    )
    error = scripty.Embed(title="Timeout Error", color=scripty.Color.GRAY_EMBED.value)

    if duration is None:
        error.description = "Unable to parse specified duration; invalid time!"
        await ctx.respond(error)
        return
    if duration < datetime.datetime.now(datetime.timezone.utc):
        error.description = "Duration provided must be in the future!"
        await ctx.respond(error)
        return
    if duration > timeout_limit:
        error.description = "Duration cannot be longer than `28 days`!"
        await ctx.respond(error)
        return

    duration_resolved = int(round(duration.timestamp()))
    duration_resolved_full = f"<t:{duration_resolved}:F>"

    await member.edit(communication_disabled_until=duration)
    await ctx.respond(
        scripty.Embed(
            title="Timeout",
            description=(
                f"Timed out **{str(member)}** until {duration_resolved_full}\n"
                f"Reason: `{reason or 'No reason provided'}`"
            ),
        )
    )


@timeout.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MODERATE_MEMBERS)
@tanjun.with_author_permission_check(hikari.Permissions.MODERATE_MEMBERS)
@tanchi.as_slash_command("remove")
async def timeout_remove(ctx: tanjun.abc.SlashContext, member: hikari.Member) -> None:
    """Remove timeout from member

    Parameters
    ----------
    member : hikari.Member
        Member to remove timeout
    """

    async def _remove_timeout() -> None:
        await member.edit(communication_disabled_until=None)
        await ctx.respond(
            scripty.Embed(
                title="Timeout",
                description=f"Removed timeout from **{str(member)}**",
            )
        )

    if member.communication_disabled_until() is None:
        await ctx.respond(
            scripty.Embed(
                title="Timeout Error",
                description="Member specified is not already timed out!",
            )
        )
    else:
        await _remove_timeout()


@functools.lru_cache
async def unban_user_autocomplete(
    ctx: tanjun.abc.AutocompleteContext,
    user: str,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Autocomplete for banned users"""
    guild = ctx.guild_id

    if guild is None:
        return

    bans = await bot.rest.fetch_bans(guild)

    ban_map = {}

    for ban in bans:
        if len(ban_map) == 10:
            break
        if user.lower() in str(ban.user).lower():
            ban_map[str(ban.user)] = str(ban.user.id)

    await ctx.set_choices(ban_map)


@component.with_command
@tanjun.with_own_permission_check(hikari.Permissions.BAN_MEMBERS)
@tanjun.with_author_permission_check(hikari.Permissions.BAN_MEMBERS)
@tanchi.as_slash_command()
async def unban(
    ctx: tanjun.abc.SlashContext,
    user: tanchi.Autocompleted[unban_user_autocomplete, hikari.Snowflake],
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Unban user from server

    Parameters
    ----------
    user : tanchi.Autocompleted[unban_user_autocomplete, hikari.Snowflake]
        User to unban
    """
    fetch_user = await bot.rest.fetch_user(user)
    guild = ctx.guild_id

    if guild is None:
        embed = scripty.Embed(
            title="Unban Error",
            description="This command must be invoked in a guild!",
        )
        await ctx.respond(embed)

    else:
        try:
            await bot.rest.unban_user(guild, user)

            embed = scripty.Embed(
                title="Unban",
                description=f"Unbanned **{str(fetch_user)}**",
            )

            await ctx.respond(embed)

        except hikari.NotFoundError:
            embed = scripty.Embed(
                title="Unban Error",
                description="Unable to unban user that is not banned!",
            )

            await ctx.respond(embed)


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
