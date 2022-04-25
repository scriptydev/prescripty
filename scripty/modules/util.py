import platform

import hikari
import miru
import psutil
import tanchi
import tanjun

import scripty


component = tanjun.Component()


@component.with_command
@tanchi.as_slash_command()
async def about(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """About the Scripty Discord bot"""
    bot_user = bot.get_me()
    assert bot_user is not None

    # if app_user is None:
    #     return None

    embed = hikari.Embed(
        title="About",
        color=scripty.Color.dark_embed(),
    )
    embed.set_author(
        name=bot_user.username,
        icon=bot_user.avatar_url or bot_user.default_avatar_url,
    )
    embed.add_field("Version", f"Scripty {scripty.__version__}", inline=True)
    embed.add_field(
        "Language", f"Python {platform.python_version()}", inline=True
    )
    embed.add_field("Library", f"Hikari {hikari.__version__}", inline=True)
    embed.add_field(
        "Developers", f"{' | '.join(scripty.__discord__)}", inline=True
    )
    embed.set_footer("We stand with 🇺🇦 Ukraine")

    await ctx.respond(embed)


class InviteView(miru.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            miru.Button(
                label="Add to Server",
                url=scripty.INVITE_URL,
            )
        )


@component.with_command
@tanchi.as_slash_command()
async def invite(ctx: tanjun.abc.SlashContext) -> None:
    """Add bot to server"""
    view = InviteView()

    embed = hikari.Embed(
        title="Invite",
        description="Invite Scripty to your Discord Server!",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed, components=view.build())


@component.with_command
@tanchi.as_slash_command()
async def ping(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Replies with bot latency"""
    embed = hikari.Embed(
        title="Ping",
        description=f"Pong! `{round(bot.heartbeat_latency * 1000)}ms`",
        color=scripty.Color.dark_embed(),
    )
    await ctx.respond(embed)


@component.with_command
@tanchi.as_slash_command()
async def system(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Bot system information"""
    system = platform.uname()

    app_user = bot.get_me()
    assert app_user is not None, "App must be started"

    # app_user = ctx.app.get_me() or await ctx.bot.rest.fetch_my_user()

    # if app_user is None:
    #     return None

    embed = hikari.Embed(
        title="System",
        color=scripty.Color.dark_embed(),
    )
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
        f"{round(psutil.virtual_memory().used / 1.074e+9, 1)}/{round(psutil.virtual_memory().total / 1.074e+9, 1)}GiB",  # type: ignore
        inline=True,
    )

    await ctx.respond(embed)


@component.with_command
@tanchi.as_slash_command()
async def uptime(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Replies with bot uptime"""
    uptime_timestamp = int(bot.uptime.timestamp())
    uptime_resolved_full = f"<t:{uptime_timestamp}:F>"
    uptime_resolved_relative = f"<t:{uptime_timestamp}:R>"
    embed = hikari.Embed(
        title="Uptime",
        description=f"Started {uptime_resolved_relative} {uptime_resolved_full}",
        color=scripty.Color.dark_embed(),
    )
    await ctx.respond(embed)


info = component.with_slash_command(
    tanjun.slash_command_group("info", "Get information")
)


@info.with_command
@tanchi.as_slash_command("member")
async def info_member(
    ctx: tanjun.abc.SlashContext,
    member: hikari.Member | None = None,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Get information about member

    Parameters
    ----------
    member : hikari.Member | None
        The member to get information about
    """
    guild = ctx.guild_id

    if guild is None:
        return

    if member:
        await bot.rest.fetch_member(guild, member)

    else:
        member = ctx.member

    assert member is not None, "Member was None"

    roles = member.get_roles()

    embed = hikari.Embed(
        title=f"Info Member",
        color=scripty.Color.dark_embed(),
    )
    embed.set_author(
        name=str(member),
        icon=member.avatar_url or member.default_avatar_url,
    )
    embed.add_field("Name", member.display_name, inline=True)
    embed.add_field("Discriminator", member.discriminator, inline=True)
    embed.add_field("ID", str(member.id), inline=True)
    embed.add_field("Nickname", str(member.nickname), inline=True)
    embed.add_field(
        "Created", f"<t:{int(member.created_at.timestamp())}:R>", inline=True
    )
    embed.add_field(
        "Joined", f"<t:{int(member.joined_at.timestamp())}:R>", inline=True
    )
    embed.add_field("Roles", " ".join(role.mention for role in roles))
    embed.add_field(
        "Permissions",
        f"Primary permission noted as `{hikari.Permissions.ADMINISTRATOR}`"
        if hikari.Permissions.ADMINISTRATOR in member.permissions  # type: ignore
        else " ".join(f"`{permission}`" for permission in member.permissions),  # type: ignore
        inline=True,
    )
    embed.set_thumbnail(member.avatar_url or member.default_avatar_url)
    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command("server")
async def info_server(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Get information about server"""
    guild = ctx.guild_id

    if guild is None:
        return

    guild = await bot.rest.fetch_guild(guild)

    embed = hikari.Embed(
        title=f"Info Server",
        color=scripty.Color.dark_embed(),
    )
    embed.add_field("Name", guild.name, inline=True)
    embed.add_field("ID", str(guild.id), inline=True)
    embed.add_field("Owner", str(await guild.fetch_owner()), inline=True)
    embed.add_field(
        "Created", f"<t:{int(guild.created_at.timestamp())}:R>", inline=True
    )
    embed.add_field(
        "Members",
        f"{guild.approximate_active_member_count}/{guild.approximate_member_count}",
        inline=True,
    )
    embed.add_field("Channels", str(len(guild.get_channels())), inline=True)
    embed.add_field("Roles", str(len(guild.get_roles())), inline=True)
    embed.add_field("Emoji", str(len(guild.emojis)), inline=True)
    embed.add_field("Region", guild.preferred_locale, inline=True)
    embed.add_field(
        "Premium Boosts", str(guild.premium_subscription_count), inline=True
    )
    embed.add_field("Premium Tier", str(guild.premium_tier), inline=True)
    embed.add_field(
        "Verification Level", str(guild.verification_level), inline=True
    )
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
    embed = hikari.Embed(
        title=f"Info Role",
        color=scripty.Color.dark_embed(),
    )
    embed.add_field("Name", role.name, inline=True)
    embed.add_field("ID", str(role.id), inline=True)
    embed.add_field(
        "Created", f"<t:{int(role.created_at.timestamp())}:R>", inline=True
    )
    embed.add_field("Color", str(role.color), inline=True)
    embed.add_field("Position", str(role.position), inline=True)
    embed.add_field("Mentionable", str(role.is_mentionable), inline=True)
    embed.add_field("Hoisted", str(role.is_hoisted), inline=True)
    embed.add_field("Managed", str(role.is_managed), inline=True)
    embed.add_field(
        "Permissions",
        f"Primary permission noted as `{hikari.Permissions.ADMINISTRATOR}`"
        if hikari.Permissions.ADMINISTRATOR in role.permissions
        else " ".join(f"`{permission}`" for permission in role.permissions),
    )
    embed.set_thumbnail(role.icon_url)

    await ctx.respond(embed)


# info channel command
@info.with_command
@tanchi.as_slash_command("channel")
async def info_channel(
    ctx: tanjun.abc.SlashContext,
    channel: hikari.GuildChannel | None = None,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """Get information about channel

    Parameters
    ----------
    channel : hikari.Channel
        The channel to get information about
    """
    if channel is None:
        channel = channel or ctx.get_channel()
    
    assert channel is not None, "Channel was None"
    
    embed = hikari.Embed(
        title=f"Info Channel",
        color=scripty.Color.dark_embed(),
    )
    embed.add_field("Name", str(channel.name), inline=True)
    embed.add_field("ID", str(channel.id), inline=True)
    embed.add_field(
        "Created", f"<t:{int(channel.created_at.timestamp())}:R>", inline=True
    )
    embed.add_field("Type", str(channel.type), inline=True)
    # embed.add_field("Position", str(channel.position), inline=True)
    # embed.add_field("NSFW", str(channel.is_nsfw), inline=True)
    # embed.add_field("Permissions", str(channel.permission_overwrites))

    await ctx.respond(embed)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
