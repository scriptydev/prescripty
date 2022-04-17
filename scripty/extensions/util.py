import platform
import psutil

import hikari
import lightbulb
import miru

import scripty


util = lightbulb.Plugin("Utility")


@util.command
@lightbulb.command("info", "Get bot statistics", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def info() -> None:
    pass


@info.child
@lightbulb.command(
    "about", "About the Scripty Discord bot", auto_defer=True, ephemeral=True
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def about(ctx: lightbulb.Context) -> None:
    app_user = ctx.app.get_me()
    assert app_user is not None, "App must be started"

    # if app_user is None:
    #     return None

    embed = hikari.Embed(
        title="About",
        color=scripty.functions.Color.background_secondary(),
    )
    embed.set_author(
        name=app_user.username, icon=app_user.avatar_url or app_user.default_avatar_url
    )
    embed.add_field("Version", f"Scripty {scripty.__version__}", inline=True)
    embed.add_field("Language", f"Python {platform.python_version()}", inline=True)
    embed.add_field("Library", f"Hikari {hikari.__version__}", inline=True)
    embed.add_field("Developers", f"{' | '.join(scripty.__discord__)}", inline=True)
    embed.set_footer("We stand with 🇺🇦 Ukraine")

    await ctx.respond(embed)


class InviteView(miru.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            miru.Button(
                label="Add to Server",
                url=scripty.constants.INVITE_URL,
            )
        )


@info.child
@lightbulb.command("invite", "Add bot to server", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def invite(ctx: lightbulb.Context) -> None:
    view = InviteView()

    embed = hikari.Embed(
        title="Invite",
        description="Invite Scripty to your Discord Server!",
        color=scripty.functions.Color.background_secondary(),
    )

    await ctx.respond(embed, components=view.build())


@info.child
@lightbulb.command("ping", "Replies with bot latency", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ping(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Ping",
        description=f"Pong! `{round(ctx.app.heartbeat_latency * 1000)}ms`",
        color=scripty.functions.Color.background_secondary(),
    )
    await ctx.respond(embed)


@info.child
@lightbulb.command("system", "Bot system information", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def system(ctx: lightbulb.Context) -> None:
    system = platform.uname()

    app_user = ctx.app.get_me()
    assert app_user is not None, "App must be started"

    # app_user = ctx.app.get_me() or await ctx.bot.rest.fetch_my_user()

    # if app_user is None:
    #     return None

    embed = hikari.Embed(
        title="System",
        color=scripty.functions.Color.background_secondary(),
    )
    embed.set_author(
        name=app_user.username, icon=app_user.avatar_url or app_user.default_avatar_url
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


@info.child
@lightbulb.command("uptime", "Replies with bot uptime", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def uptime(ctx: lightbulb.Context) -> None:
    uptime_resolved_full = f"<t:{ctx.app.d.uptime}:F>"
    uptime_resolved_relative = f"<t:{ctx.app.d.uptime}:R>"
    embed = hikari.Embed(
        title="Uptime",
        description=f"Started {uptime_resolved_relative} {uptime_resolved_full}",
        color=scripty.functions.Color.background_secondary(),
    )
    await ctx.respond(embed)


def load(bot: scripty.core.BotApp):
    bot.add_plugin(util)


def unload(bot: scripty.core.BotApp):
    bot.remove_plugin(util)
