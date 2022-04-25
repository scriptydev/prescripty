import asyncio
import datetime
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
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
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

    if not guild:
        return

    await bot.rest.ban_user(
        guild, user, delete_message_days=delete_message_days, reason=reason
    )

    embed = hikari.Embed(
        title="Ban",
        description=f"Banned **{str(user)}** \n Reason: `{reason or 'No reason provided'}`",
        color=scripty.functions.Color.background_secondary(),
    )

    await ctx.respond(embed)


@component.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MANAGE_MESSAGES)
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_MESSAGES)
@tanchi.as_slash_command()
async def delete(
    ctx: tanjun.abc.SlashContext,
    amount: tanchi.Range[1, ...],
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
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

    def generate_embed(message: str) -> hikari.Embed:
        return hikari.Embed(
            title="Delete",
            description=message,
            color=scripty.functions.Color.background_secondary(),
        )

    if tasks:
        await asyncio.wait(tasks)

        if count < amount:
            if count == 1:
                await ctx.respond(
                    generate_embed(
                        f"`{count} message` deleted \n Older messages past `14 days` cannot be deleted"
                    )
                )

            else:
                await ctx.respond(
                    generate_embed(
                        f"`{count} messages` deleted \n Older messages past `14 days` cannot be deleted"
                    )
                )

        elif count == 1:
            await ctx.respond(generate_embed(f"`{count} message` deleted"))

        else:
            await ctx.respond(generate_embed(f"`{count} messages` deleted"))

    else:
        embed = hikari.Embed(
            title="Delete Error",
            description="Unable to delete messages! \n Messages are older than `14 days` or do not exist",
            color=scripty.functions.Color.background_secondary(),
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
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
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
        return

    await bot.rest.kick_user(guild, member)

    embed = hikari.Embed(
        title="Kick",
        description=f"Kicked **{str(member)}** \n Reason: `{reason or 'No reason provided'}`",
        color=scripty.functions.Color.background_secondary(),
    )

    await ctx.respond(embed)


slowmode = component.with_slash_command(tanjun.slash_command_group("slowmode", "Slowmode channel"))


@slowmode.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanchi.as_slash_command("enable")
async def slowmode_enable(
    ctx: tanjun.abc.SlashContext,
    duration: tanchi.Range[1, 21600],
    channel: hikari.TextableGuildChannel | None = None,
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
) -> None:
    """Set slowmode for channel

    Parameters
    ----------
    channel : hikari.TextableGuildChannel
        Channel to set slowmode
    duration : tanchi.Range[int, ...]
        Duration of slowmode
    """
    channel = channel or ctx.get_channel()
    assert isinstance(channel, hikari.TextableGuildChannel)

    await bot.rest.edit_channel(channel, rate_limit_per_user=duration)

    embed = hikari.Embed(
        title="Slowmode",
        description=f"Set slowmode for **{str(channel)}** to `{duration}s`",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed)


@slowmode.with_command
@tanjun.with_own_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_CHANNELS)
@tanchi.as_slash_command("disable")
async def slowmode_disable(
    ctx: tanjun.abc.SlashContext,
    channel: hikari.TextableGuildChannel | None = None,
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
) -> None:
    """Remove slowmode from channel

    Parameters
    ----------
    channel : hikari.TextableGuildChannel
        Channel to remove slowmode
    """
    channel = channel or ctx.get_channel()
    assert isinstance(channel, hikari.TextableGuildChannel)

    await bot.rest.edit_channel(channel, rate_limit_per_user=0)

    embed = hikari.Embed(
        title="Slowmode",
        description=f"Removed slowmode from **{str(channel)}**",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed)


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
    duration: tanchi.Converted[datetime.datetime, scripty.parse_duration],
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
    timeout_limit = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(days=28)

    if not duration:
        embed = hikari.Embed(
            title="Timeout Error",
            description="Unable to parse specified duration; invalid time!",
            color=scripty.functions.Color.background_secondary(),
        )
        await ctx.respond(embed)

    elif duration < datetime.datetime.now(datetime.timezone.utc):
        embed = hikari.Embed(
            title="Timeout Error",
            description="Duration provided must be in the future!",
            color=scripty.functions.Color.background_secondary(),
        )
        await ctx.respond(embed)

    elif duration > timeout_limit:
        embed = hikari.Embed(
            title="Timeout Error",
            description="Duration cannot be longer than `28 days`!",
            color=scripty.functions.Color.background_secondary(),
        )
        await ctx.respond(embed)

    else:
        duration_resolved = int(round(duration.timestamp()))
        duration_resolved_full = f"<t:{duration_resolved}:F>"

        await member.edit(communication_disabled_until=duration)

        embed = hikari.Embed(
            title="Timeout",
            description=f"Timed out **{str(member)}** until {duration_resolved_full} \n Reason: `{reason or 'No reason provided'}`",
            color=scripty.functions.Color.background_secondary(),
        )

        await ctx.respond(embed)


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
    if not member.communication_disabled_until():
        embed = hikari.Embed(
            title="Timeout Error",
            description="You cannot remove timeout from member that is not timed out!",
            color=scripty.functions.Color.background_secondary(),
        )
        await ctx.respond(embed)

    else:
        await member.edit(communication_disabled_until=None)

        embed = hikari.Embed(
            title="Timeout",
            description=f"Removed timeout from **{str(member)}**",
            color=scripty.functions.Color.background_secondary(),
        )

        await ctx.respond(embed)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
