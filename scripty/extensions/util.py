import platform
import psutil

import hikari
import lightbulb
import miru

import scripty
from scripty import functions
from scripty.constants import INVITE_URL


util = lightbulb.Plugin("Utility")


@util.command
@lightbulb.command("about", "About the Scripty Discord bot", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def about(ctx: lightbulb.Context) -> None:
    app_user = ctx.app.get_me()
    assert app_user is not None, "App must be started"

    embed = hikari.Embed(
        title="About",
        color=functions.Color.blurple(),
    )
    embed.set_author(name=app_user.username, icon=app_user.avatar_url)
    embed.add_field("Version", f"Scripty {scripty.__version__}", inline=True)
    embed.add_field("Language", f"Python {platform.python_version()}", inline=True)
    embed.add_field("Library", f"Hikari {hikari.__version__}", inline=True)
    embed.add_field("Developers", f"{' | '.join(scripty.__discord__)}", inline=True)
    embed.set_footer("We stand with 🇺🇦 Ukraine")

    await ctx.respond(embed)


@util.command
@lightbulb.command("system", "Bot system information", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def system(ctx: lightbulb.Context) -> None:
    system = platform.uname()

    app_user = ctx.app.get_me()
    assert app_user is not None, "App must be started"

    embed = hikari.Embed(
        title="System",
        color=functions.Color.blurple(),
    )
    embed.set_author(name=app_user.username, icon=app_user.avatar_url)
    embed.add_field("System", system.system, inline=True)
    embed.add_field("Release", system.version, inline=True)
    embed.add_field("Machine", system.machine, inline=True)
    embed.add_field("Processor", system.processor, inline=True)
    embed.add_field("CPU", f"{psutil.cpu_percent()}%", inline=True)
    embed.add_field(
        "Memory",
        f"{round(psutil.virtual_memory().used / 1.074e+9, 1)}/{round(psutil.virtual_memory().total / 1.074e+9, 1)}GiB", # type: ignore
        inline=True,
    )

    await ctx.respond(embed)


class InviteView(miru.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            miru.Button(
                label="Add to Server",
                url=INVITE_URL,
            )
        )


@util.command
@lightbulb.command("invite", "Add bot to server", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def invite(ctx: lightbulb.Context) -> None:
    view = InviteView()

    embed = hikari.Embed(
        title="Invite",
        description="Invite Scripty to your Discord Server!",
        color=functions.Color.blurple(),
    )

    await ctx.respond(embed, components=view.build())


@util.command
@lightbulb.command("ping", "Replies with bot latency", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Ping",
        description=f"Pong! `{round(ctx.app.heartbeat_latency * 1000)}ms`",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@util.command
@lightbulb.command("uptime", "Replies with bot uptime", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def uptime(ctx: lightbulb.Context) -> None:
    uptime_resolved_full = f"<t:{ctx.app.d.uptime}:F>"
    uptime_resolved_relative = f"<t:{ctx.app.d.uptime}:R>"
    embed = hikari.Embed(
        title="Uptime",
        description=f"Started {uptime_resolved_relative} {uptime_resolved_full}",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(util)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(util)
