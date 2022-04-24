import platform

import hikari
import miru
import psutil
import tanchi
import tanjun

import scripty


component = tanjun.Component()

info = component.with_slash_command(
    tanjun.slash_command_group("info", "Get bot statistics.")
)


@info.with_command
@tanchi.as_slash_command()
async def about(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
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


@info.with_command
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


@info.with_command
@tanchi.as_slash_command()
async def ping(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
) -> None:
    """Replies with bot latency"""
    embed = hikari.Embed(
        title="Ping",
        description=f"Pong! `{round(bot.heartbeat_latency * 1000)}ms`",
        color=scripty.Color.dark_embed(),
    )
    await ctx.respond(embed)


@info.with_command
@tanchi.as_slash_command()
async def system(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
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


@info.with_command
@tanchi.as_slash_command()
async def uptime(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.Bot = tanjun.inject(type=scripty.Bot),
) -> None:
    """Replies with bot uptime"""
    uptime_resolved_full = f"<t:{bot.uptime}:F>"
    uptime_resolved_relative = f"<t:{bot.uptime}:R>"
    embed = hikari.Embed(
        title="Uptime",
        description=f"Started {uptime_resolved_relative} {uptime_resolved_full}",
        color=scripty.Color.dark_embed(),
    )
    await ctx.respond(embed)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
