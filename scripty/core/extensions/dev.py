import hikari
import lightbulb

import scripty


dev = lightbulb.Plugin("Developer", default_enabled_guilds=scripty.constants.DEV_ID)


@dev.command
@lightbulb.option("extension", "The extension to load", str, required=True)
@lightbulb.command("load", "Load an extension", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def load_(ctx: lightbulb.Context) -> None:
    extension = ctx.options.extension

    embed = hikari.Embed(
        title="Load",
        description=f"`{extension}` extension loaded",
        color=scripty.functions.Color.background_secondary(),
    )

    await ctx.respond(embed)


@dev.command
@lightbulb.option("extension", "The extension to unload", str, required=True)
@lightbulb.command("unload", "Unload an extension", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unload_(ctx: lightbulb.Context) -> None:
    extension = ctx.options.extension

    ctx.app.unload_extensions(f"scripty.extensions.{extension}")

    embed = hikari.Embed(
        title="Unload",
        description=f"`{extension}` extension unloaded",
        color=scripty.functions.Color.background_secondary(),
    )

    await ctx.respond(embed)


@dev.command
@lightbulb.option("extension", "The extension to reload", str, required=True)
@lightbulb.command("reload", "Reload an extension", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def reload_(ctx: lightbulb.Context) -> None:
    extension = ctx.options.extension
    extension = extension.lower()

    ctx.app.reload_extensions(f"scripty.extensions.{extension}")

    embed = hikari.Embed(
        title="Reload",
        description=f"`{extension}` extension reloaded",
        color=scripty.functions.Color.background_secondary(),
    )

    await ctx.respond(embed)


def load(bot: scripty.core.BotApp):
    bot.add_plugin(dev)


def unload(bot: scripty.core.BotApp):
    bot.remove_plugin(dev)
