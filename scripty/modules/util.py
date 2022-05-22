__all__: list[str] = ["loader_util"]

import datetime
import platform

from typing import Sequence

import alluka
import hikari
import miru
import psutil
import tanchi
import tanjun

import scripty

stats = tanjun.slash_command_group("stats", "Statistics related to Scripty")
info = tanjun.slash_command_group("info", "Get information")


class InviteView(miru.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            miru.Button(
                label="Add Scripty to Server",
                url=scripty.INVITE_URL,
            )
        )


@stats.with_command
@tanchi.as_slash_command("about")
async def stats_about(
    ctx: tanjun.abc.SlashContext,
    bot: alluka.Injected[hikari.GatewayBot],
) -> None:
    """About the Scripty Discord bot"""
    bot_user = bot.get_me() or await bot.rest.fetch_my_user()

    view = InviteView()

    embed = (
        scripty.Embed(title="About")
        .set_author(
            name=bot_user.username,
            icon=bot_user.avatar_url or bot_user.default_avatar_url,
        )
        .add_field("Version", f"Scripty {scripty.__version__}", inline=True)
        .add_field("Language", f"Python {platform.python_version()}", inline=True)
        .add_field("Library", f"Hikari {hikari.__version__}", inline=True)
        .add_field("Repository", f"[GitHub]({scripty.__repository__})", inline=True)
        .add_field("Guilds", str(await bot.rest.fetch_my_guilds().count()), inline=True)
        .add_field("Developer", scripty.__discord__, inline=True)
        .add_field(
            "Created", scripty.discord_timestamp(bot_user.created_at, "F"), inline=True
        )
        .set_footer("#StandWithUkraine")
    )

    await ctx.respond(embed, components=view.build())


@stats.with_command
@tanchi.as_slash_command("ping")
async def stats_ping(
    ctx: tanjun.abc.SlashContext,
    bot: alluka.Injected[hikari.GatewayBot],
) -> None:
    """Replies with bot latency"""
    await ctx.respond(
        scripty.Embed(
            title="Ping",
            description=f"Pong! `{round(bot.heartbeat_latency * 1000)}ms`",
        )
    )


@stats.with_command
@tanchi.as_slash_command("system")
async def stats_system(
    ctx: tanjun.abc.SlashContext,
    bot: alluka.Injected[hikari.GatewayBot],
    datastore: alluka.Injected[scripty.DataStore],
) -> None:
    """Bot system information"""
    app_user = bot.get_me() or await bot.rest.fetch_my_user()

    boot_timestamp = psutil.boot_time()
    boot_resolved_relative = scripty.discord_timestamp(
        datetime.datetime.fromtimestamp(boot_timestamp), "R"
    )

    start_time_timestamp = datastore.start_time
    start_time_resolved_relative = scripty.discord_timestamp(start_time_timestamp, "R")

    embed = (
        scripty.Embed(title="System")
        .set_author(
            name=app_user.username,
            icon=app_user.avatar_url or app_user.default_avatar_url,
        )
        .add_field("System", platform.system(), inline=True)
        .add_field("Platform", platform.platform(aliased=True, terse=True), inline=True)
        .add_field("Machine", platform.machine(), inline=True)
        .add_field("Processor", platform.processor(), inline=True)
        .add_field("CPU", f"{psutil.cpu_percent(interval=None)}%", inline=True)
        .add_field(
            "Memory",
            f"{round(psutil.virtual_memory().used / 1.074e+9, 1)}/"  # type: ignore
            f"{round(psutil.virtual_memory().total / 1.074e+9, 1)}GiB",  # type: ignore
            inline=True,
        )
        .add_field(
            "Host",
            f"Booted {boot_resolved_relative}",
            inline=True,
        )
        .add_field(
            "Process",
            f"Online {start_time_resolved_relative}",
            inline=True,
        )
    )

    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command("user")
async def info_user(
    ctx: tanjun.abc.SlashContext,
    user: hikari.User | None = None,
) -> None:
    """Get information about user

    Parameters
    ----------
    user : hikari.User | None
        The user to get information about
    """
    if not user:
        user = ctx.member or ctx.author

    member: bool = isinstance(user, hikari.InteractionMember)
    roles: Sequence[hikari.Role] = user.get_roles() if member else []

    embed = (
        scripty.Embed(title="Info")
        .set_author(
            name=str(user),
            icon=user.avatar_url or user.default_avatar_url,
        )
        .add_field("Name", user.username, inline=True)
        .add_field("Discriminator", user.discriminator, inline=True)
        .add_field("ID", str(user.id), inline=True)
        .add_field(
            "Created", scripty.discord_timestamp(user.created_at, "R"), inline=True
        )
        .set_thumbnail(user.avatar_url or user.default_avatar_url)
    )

    if member:
        embed.add_field(
            "Joined", scripty.discord_timestamp(user.joined_at, "R"), inline=True
        )
        embed.add_field("Nickname", str(user.nickname), inline=True)
        embed.add_field("Roles", " ".join(role.mention for role in roles))
        embed.add_field(
            "Permissions",
            " ".join(f"`{permission}`" for permission in user.permissions),
        )

    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command("server")
async def info_server(
    ctx: tanjun.abc.SlashContext,
    bot: alluka.Injected[hikari.GatewayBot],
) -> None:
    """Get information about server"""
    guild = ctx.guild_id

    if guild is None:
        await ctx.respond(
            scripty.Embed(
                title="Info",
                description="This command was not invoked in a guild!",
            )
        )
        return

    guild = await bot.rest.fetch_guild(guild)

    embed = (
        scripty.Embed(title="Info")
        .add_field("Name", guild.name, inline=True)
        .add_field("ID", str(guild.id), inline=True)
        .add_field("Owner", str(await guild.fetch_owner()), inline=True)
        .add_field(
            "Created", scripty.discord_timestamp(guild.created_at, "R"), inline=True
        )
        .add_field(
            "Members",
            f"{guild.approximate_active_member_count}/"
            f"{guild.approximate_member_count}",
            inline=True,
        )
        .add_field("Channels", str(len(guild.get_channels())), inline=True)
        .add_field("Roles", str(len(guild.get_roles())), inline=True)
        .add_field("Emoji", str(len(guild.emojis)), inline=True)
        .add_field("Region", guild.preferred_locale, inline=True)
        .add_field("Premium Boosts", str(guild.premium_subscription_count), inline=True)
        .add_field("Premium Tier", str(guild.premium_tier), inline=True)
        .add_field("Verification Level", str(guild.verification_level), inline=True)
        .set_thumbnail(guild.icon_url)
    )

    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command("role")
async def info_role(
    ctx: tanjun.abc.SlashContext,
    role: hikari.Role,
) -> None:
    """Get information about role

    Parameters
    ----------
    role : hikari.Role
        The role to get information about
    """
    embed = (
        scripty.Embed(title="Info")
        .add_field("Name", role.name, inline=True)
        .add_field("ID", str(role.id), inline=True)
        .add_field(
            "Created", scripty.discord_timestamp(role.created_at, "R"), inline=True
        )
        .add_field("Color", str(role.color), inline=True)
        .add_field("Position", str(role.position), inline=True)
        .add_field("Mentionable", str(role.is_mentionable), inline=True)
        .add_field("Hoisted", str(role.is_hoisted), inline=True)
        .add_field("Managed", str(role.is_managed), inline=True)
        .add_field(
            "Permissions",
            " ".join(f"`{permission}`" for permission in role.permissions),
        )
        .set_thumbnail(role.icon_url)
    )

    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command("channel")
async def info_channel(
    ctx: tanjun.abc.SlashContext,
    channel: hikari.GuildChannel | None = None,
) -> None:
    """Get information about channel

    Parameters
    ----------
    channel : hikari.Channel
        The channel to get information about
    """
    channel = channel or ctx.get_channel()

    if channel is None:
        await ctx.respond(
            scripty.Embed(
                title="Info Error",
                description=(
                    "This command must be invoked in a valid textable guild channel!"
                ),
            )
        )
        return

    embed = (
        scripty.Embed(title="Info")
        .add_field("Name", str(channel.name), inline=True)
        .add_field("ID", str(channel.id), inline=True)
        .add_field(
            "Created", scripty.discord_timestamp(channel.created_at, "R"), inline=True
        )
        .add_field("Type", str(channel.type), inline=True)
    )

    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command("invite")
async def info_invite(
    ctx: tanjun.abc.SlashContext,
    invite: hikari.Invite,
) -> None:
    """Get information about invite

    Parameters
    ----------
    invite : hikari.Invite
        The invite to get information about
    """
    embed = (
        scripty.Embed(title="Info")
        .add_field("Code", invite.code, inline=True)
        .add_field("Inviter", str(invite.inviter), inline=True)
        .add_field("Target", str(invite.target_user), inline=True)
        .add_field("Guild", str(invite.guild), inline=True)
        .add_field("Channel", str(invite.channel), inline=True)
        .add_field(
            "Expire",
            scripty.discord_timestamp(invite.expires_at, "R")
            if invite.expires_at
            else str(invite.expires_at),
            inline=True,
        )
    )

    await ctx.respond(embed)


loader_util = tanjun.Component(name="util").load_from_scope().make_loader()
