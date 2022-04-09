import platform
import psutil

import hikari
import lightbulb
import miru

import scripty
from scripty import functions


util = lightbulb.Plugin("Utility")


@util.command()
@lightbulb.command("bot", "Functions related to Scripty", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def bot() -> None:
    pass


@bot.child()
@lightbulb.command("about", "About the Scripty Discord bot", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def about(ctx: lightbulb.Context) -> None:
    app_user = ctx.app.get_me()

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


@bot.child()
@lightbulb.command("system", "System info pertaining to the bot", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def system(ctx: lightbulb.Context) -> None:
    system = platform.uname()

    app_user = ctx.app.get_me()

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
        f"{round(psutil.virtual_memory().used / 1.074e+9, 1)}/{round(psutil.virtual_memory().total / 1.074e+9, 1)}GiB",
        inline=True,
    )

    await ctx.respond(embed)


class InviteView(miru.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            miru.Button(
                label="Add to Server",
                url="https://discord.com/api/oauth2/authorize?client_id=883496337616822302&permissions=8&scope=bot%20applications.commands",
            )
        )


@bot.child()
@lightbulb.command("invite", "Add the bot to server", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def invite(ctx: lightbulb.Context) -> None:
    view = InviteView()

    embed = hikari.Embed(
        title="Invite",
        description="Invite Scripty to your Discord Server!",
        color=functions.Color.blurple(),
    )

    await ctx.respond(embed, components=view.build())


@bot.child()
@lightbulb.command("ping", "Replies with bot latency", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ping(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Ping",
        description=f"Pong! `{round(ctx.app.heartbeat_latency * 1000)}ms`",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@bot.child()
@lightbulb.command("uptime", "Replies with bot uptime", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def uptime(ctx: lightbulb.Context) -> None:
    uptime_resolved_full = f"<t:{ctx.app.uptime}:F>"
    uptime_resolved_relative = f"<t:{ctx.app.uptime}:R>"
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
