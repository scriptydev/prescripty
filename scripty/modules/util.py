import platform

import alluka
import hikari
import miru
import psutil
import tanchi
import tanjun

import scripty


component = tanjun.Component()


stats = component.with_slash_command(
    tanjun.slash_command_group("stats", "Statistics related to Scripty")
)


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
    bot: alluka.Injected[scripty.AppBot],
) -> None:
    """About the Scripty Discord bot"""
    bot_user = bot.get_me() or await bot.rest.fetch_my_user()

    view = InviteView()

    embed = scripty.Embed(title="About")
    embed.set_author(
        name=bot_user.username,
        icon=bot_user.avatar_url or bot_user.default_avatar_url,
    )
    embed.add_field("Version", f"Scripty {scripty.__version__}", inline=True)
    embed.add_field("Language", f"Python {platform.python_version()}", inline=True)
    embed.add_field("Library", f"Hikari {hikari.__version__}", inline=True)
    embed.add_field("Repository", f"[GitHub]({scripty.__repository__})", inline=True)
    embed.add_field(
        "Guilds", str(await bot.rest.fetch_my_guilds().count()), inline=True
    )
    embed.add_field(
        "Developers",
        " ".join(f"`{dev}`" for dev in scripty.__discord__),
        inline=True,
    )
    embed.set_footer("#StandWithUkraine")

    await ctx.respond(embed, components=view.build())


@stats.with_command
@tanchi.as_slash_command("ping")
async def stats_ping(
    ctx: tanjun.abc.SlashContext,
    bot: alluka.Injected[scripty.AppBot],
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
    bot: alluka.Injected[scripty.AppBot],
) -> None:
    """Bot system information"""
    app_user = bot.get_me() or await bot.rest.fetch_my_user()

    system = platform.uname()

    boot_timestamp = round(psutil.boot_time())
    boot_resolved_full = f"<t:{boot_timestamp}:F>"
    boot_resolved_relative = f"<t:{boot_timestamp}:R>"

    uptime_timestamp = round(bot.uptime.timestamp())
    uptime_resolved_full = f"<t:{uptime_timestamp}:F>"
    uptime_resolved_relative = f"<t:{uptime_timestamp}:R>"

    embed = scripty.Embed(title="System")
    embed.set_author(
        name=app_user.username,
        icon=app_user.avatar_url or app_user.default_avatar_url,
    )
    embed.add_field("System", system.system, inline=True)
    embed.add_field("Release", system.version, inline=True)
    embed.add_field("Machine", system.machine, inline=True)
    embed.add_field("Processor", system.processor, inline=True)
    embed.add_field("CPU", f"{psutil.cpu_percent()}%", inline=True)
    embed.add_field(
        "Memory",
        f"{round(psutil.virtual_memory().used / 1.074e+9, 1)}/"  # type: ignore
        f"{round(psutil.virtual_memory().total / 1.074e+9, 1)}GiB",  # type: ignore
        inline=True,
    )
    embed.add_field(
        "Boot Time",
        f"Started {boot_resolved_relative} {boot_resolved_full}",
    )
    embed.add_field(
        "Uptime",
        f"Online {uptime_resolved_relative} {uptime_resolved_full}",
    )

    await ctx.respond(embed)


info = component.with_slash_command(
    tanjun.slash_command_group("info", "Get information")
)


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

    member = isinstance(user, hikari.Member)

    roles = user.get_roles() if member else [None]

    embed = scripty.Embed(title="Info")
    embed.set_author(
        name=str(user),
        icon=user.avatar_url or user.default_avatar_url,
    )
    embed.add_field("Name", user.username, inline=True)
    embed.add_field("Discriminator", user.discriminator, inline=True)
    embed.add_field("ID", str(user.id), inline=True)
    embed.add_field("Created", f"<t:{int(user.created_at.timestamp())}:R>", inline=True)
    embed.add_field(
        "Joined",
        f"<t:{int(user.joined_at.timestamp())}:R>" if member else "`Not in Guild`",
        inline=True,
    )
    embed.add_field(
        "Nickname",
        str(user.nickname) if member else "`Not in Guild`",
        inline=True,
    )
    embed.add_field(
        "Roles",
        " ".join(role.mention for role in roles if role)
        if member
        else "`Not in Guild`",
    )
    embed.add_field(
        "Permissions",
        " ".join(f"`{permission}`" for permission in user.permissions)  # type: ignore
        if isinstance(user, hikari.Member)
        else "`Not in Guild`",
    )
    embed.set_thumbnail(user.avatar_url or user.default_avatar_url)

    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command("server")
async def info_server(
    ctx: tanjun.abc.SlashContext,
    bot: alluka.Injected[scripty.AppBot],
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

    embed = scripty.Embed(title="Info")
    embed.add_field("Name", guild.name, inline=True)
    embed.add_field("ID", str(guild.id), inline=True)
    embed.add_field("Owner", str(await guild.fetch_owner()), inline=True)
    embed.add_field(
        "Created",
        f"<t:{int(guild.created_at.timestamp())}:R>",
        inline=True,
    )
    embed.add_field(
        "Members",
        f"{guild.approximate_active_member_count}/" f"{guild.approximate_member_count}",
        inline=True,
    )
    embed.add_field("Channels", str(len(guild.get_channels())), inline=True)
    embed.add_field("Roles", str(len(guild.get_roles())), inline=True)
    embed.add_field("Emoji", str(len(guild.emojis)), inline=True)
    embed.add_field("Region", guild.preferred_locale, inline=True)
    embed.add_field(
        "Premium Boosts",
        str(guild.premium_subscription_count),
        inline=True,
    )
    embed.add_field("Premium Tier", str(guild.premium_tier), inline=True)
    embed.add_field("Verification Level", str(guild.verification_level), inline=True)
    embed.set_thumbnail(guild.icon_url)

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
    embed = scripty.Embed(title="Info")
    embed.add_field("Name", role.name, inline=True)
    embed.add_field("ID", str(role.id), inline=True)
    embed.add_field("Created", f"<t:{int(role.created_at.timestamp())}:R>", inline=True)
    embed.add_field("Color", str(role.color), inline=True)
    embed.add_field("Position", str(role.position), inline=True)
    embed.add_field("Mentionable", str(role.is_mentionable), inline=True)
    embed.add_field("Hoisted", str(role.is_hoisted), inline=True)
    embed.add_field("Managed", str(role.is_managed), inline=True)
    embed.add_field(
        "Permissions",
        " ".join(f"`{permission}`" for permission in role.permissions),
    )
    embed.set_thumbnail(role.icon_url)

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
                description="This command must be invoked in a guild!",
            )
        )
        return

    embed = scripty.Embed(title="Info")
    embed.add_field("Name", str(channel.name), inline=True)
    embed.add_field("ID", str(channel.id), inline=True)
    embed.add_field(
        "Created",
        f"<t:{int(channel.created_at.timestamp())}:R>",
        inline=True,
    )
    embed.add_field("Type", str(channel.type), inline=True)

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
    embed = scripty.Embed(title="Info")
    embed.add_field("Code", invite.code, inline=True)
    embed.add_field("Inviter", str(invite.inviter), inline=True)
    embed.add_field("Target", str(invite.target_user), inline=True)
    embed.add_field("Guild", str(invite.guild), inline=True)
    embed.add_field("Channel", str(invite.channel), inline=True)
    embed.add_field(
        "Expire",
        f"<t:{int(invite.expires_at.timestamp())}:R>"
        if invite.expires_at
        else str(invite.expires_at),
        inline=True,
    )

    await ctx.respond(embed)


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
