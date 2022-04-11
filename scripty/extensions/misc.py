# import typing
import hikari
import lightbulb

import scripty
from scripty import functions


misc = lightbulb.Plugin("Miscellaneous")


@misc.command
@lightbulb.command("Avatar", "Retrieves user avatar", auto_defer=True)
@lightbulb.implements(lightbulb.UserCommand)
async def avatar(ctx: lightbulb.Context) -> None:
    user: hikari.User = ctx.options.target

    embed = hikari.Embed(
        title=f"Avatar",
        color=functions.Color.blurple(),
    )
    embed.set_author(name=str(user), icon=user.avatar_url)
    embed.set_image(user.avatar_url)

    await ctx.respond(embed)


@misc.command
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)
@lightbulb.option("text", "Text to repeat", str)
@lightbulb.command("echo", "Repeats user input", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    text: str = ctx.options.text
    embed = hikari.Embed(
        title="Echo",
        description=f"```{text}```",
        color=functions.Color.blurple(),
    )
    embed.set_author(name=str(ctx.author), icon=ctx.author.avatar_url)
    await ctx.respond(embed)


@echo.set_error_handler
async def on_echo_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CheckFailure):
        embed = hikari.Embed(
            title="Echo Error",
            description="`MANAGE_MESSAGES` permission missing!",
            color=functions.Color.red(),
        )
        await event.context.respond(embed)


@misc.command
@lightbulb.option("option_j", "Option J", str, required=False)
@lightbulb.option("option_i", "Option I", str, required=False)
@lightbulb.option("option_h", "Option H", str, required=False)
@lightbulb.option("option_g", "Option G", str, required=False)
@lightbulb.option("option_f", "Option F", str, required=False)
@lightbulb.option("option_e", "Option E", str, required=False)
@lightbulb.option("option_d", "Option D", str, required=False)
@lightbulb.option("option_c", "Option C", str, required=False)
@lightbulb.option("option_b", "Option B", str)
@lightbulb.option("option_a", "Option A", str)
@lightbulb.option("topic", "Topic of the poll", str)
@lightbulb.command("poll", "Create a simple poll", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def poll(ctx: lightbulb.Context) -> None:
    topic: str = ctx.options.topic
    options: dict[str, str] = {
        "\U0001f1e6": ctx.options.option_a,
        "\U0001f1e7": ctx.options.option_b,
        "\U0001f1e8": ctx.options.option_c,
        "\U0001f1e9": ctx.options.option_d,
        "\U0001f1ea": ctx.options.option_e,
        "\U0001f1eb": ctx.options.option_f,
        "\U0001f1ec": ctx.options.option_g,
        "\U0001f1ed": ctx.options.option_h,
        "\U0001f1ee": ctx.options.option_i,
        "\U0001f1ef": ctx.options.option_j,
    }

    embed = hikari.Embed(
        title=topic,
        description="\n\n".join(
            f"{key} {value}" for key, value in options.items() if value is not None
        ),
        color=functions.Color.blurple(),
    )
    embed.set_author(name=str(ctx.author), icon=ctx.author.avatar_url)

    await ctx.respond(embed)

    for key, value in options.items():
        if value is not None:
            response = await ctx.interaction.fetch_initial_response()
            await response.add_reaction(key)


def load(bot: scripty.BotApp):
    bot.add_plugin(misc)


def unload(bot: scripty.BotApp):
    bot.remove_plugin(misc)
