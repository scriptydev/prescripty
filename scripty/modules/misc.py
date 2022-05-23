from __future__ import annotations

__all__: tuple[str, ...] = ("loader_misc",)

import hikari
import tanchi
import tanjun

from gpytranslate import Translator

import scripty


@tanjun.as_user_menu("Avatar")
async def avatar(
    ctx: tanjun.abc.MenuContext, user: hikari.User | hikari.InteractionMember
) -> None:
    """Get user avatar"""
    await ctx.respond(
        scripty.Embed(title="Avatar")
        .set_author(name=str(user), icon=user.avatar_url or user.default_avatar_url)
        .set_image(user.avatar_url or user.default_avatar_url)
    )


@tanjun.as_message_menu("Translate to English")
async def translate_menu(
    ctx: tanjun.abc.MenuContext,
    message: hikari.Message,
) -> None:
    """Translate message to English"""
    translator = Translator()

    if not message.content:
        await ctx.respond(
            scripty.Embed(
                title="Translate Error",
                description="Message is empty",
            )
        )
        return

    translate = await translator.translate(  # type: ignore
        message.content, targetlang="en"
    )
    translate_lang = await translator.detect(message.content)  # type: ignore

    embed = (
        scripty.Embed(title="Translate")
        .set_author(
            name=str(message.author),
            icon=message.author.avatar_url or message.author.default_avatar_url,
        )
        .add_field(
            f"Original <- {translate_lang.upper()}",  # type: ignore
            f"```{translate.orig}```",  # type: ignore
        )
        .add_field("Translated -> EN", f"```{translate.text}```")  # type: ignore
    )

    await ctx.respond(embed)


@tanchi.as_slash_command("translate")
async def translate_slash(
    ctx: tanjun.abc.Context,
    text: str,
    source: str = "auto",
    target: str = "en",
) -> None:
    """Translate message to specified language

    Parameters
    ----------
    text : str
        Text to translate
    source : str
        Language to translate from
    target : str
        Language to translate to
    """
    translator = Translator()
    translate = await translator.translate(  # type: ignore
        text, sourcelang=source, targetlang=target
    )
    translate_lang = await translator.detect(text)  # type: ignore

    embed = (
        scripty.Embed(title="Translate")
        .set_author(
            name=str(ctx.author),
            icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
        )
        .add_field(
            f"Original <- {translate_lang.upper()}",  # type: ignore
            f"```{translate.orig}```",  # type: ignore
        )
        .add_field(
            f"Translated -> {target.upper()}", f"```{translate.text}```"  # type: ignore
        )
    )

    await ctx.respond(embed)


@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_MESSAGES)
@tanchi.as_slash_command()
async def echo(ctx: tanjun.abc.SlashContext, text: str) -> None:
    """Repeats user input

    Parameters
    ----------
    text : str
        Text to repeat
    """
    embed = scripty.Embed(title="Echo", description=f"```{text}```").set_author(
        name=str(ctx.author),
        icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
    )

    await ctx.respond(embed)


@tanchi.as_slash_command()
async def poll(
    ctx: tanjun.abc.SlashContext,
    topic: str,
    option_a: str,
    option_b: str,
    option_c: str | None = None,
    option_d: str | None = None,
    option_e: str | None = None,
    option_f: str | None = None,
    option_g: str | None = None,
    option_h: str | None = None,
    option_i: str | None = None,
    option_j: str | None = None,
) -> None:
    """Create a simple poll

    Parameters
    ----------
    topic : str
        Topic of the poll
    option_a : str
        Option A
    option_b : str
        Option B
    option_c : str | None
        Option C
    option_d : str | None
        Option D
    option_e : str | None
        Option E
    option_f : str | None
        Option F
    option_g : str | None
        Option G
    option_h : str | None
        Option H
    option_i : str | None
        Option I
    option_j : str | None
        Option J
    """
    options: dict[str, str | None] = {
        "\U0001f1e6": option_a,
        "\U0001f1e7": option_b,
        "\U0001f1e8": option_c,
        "\U0001f1e9": option_d,
        "\U0001f1ea": option_e,
        "\U0001f1eb": option_f,
        "\U0001f1ec": option_g,
        "\U0001f1ed": option_h,
        "\U0001f1ee": option_i,
        "\U0001f1ef": option_j,
    }

    embed = scripty.Embed(
        title=topic,
        description="\n\n".join(
            f"{key} {value}" for key, value in options.items() if value is not None
        ),
    ).set_author(
        name=str(ctx.author),
        icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
    )

    response = await ctx.respond(embed, ensure_result=True)

    for key, value in options.items():
        if value is not None:
            try:
                await response.add_reaction(key)
            except hikari.NotFoundError:
                pass


loader_misc = tanjun.Component(name="misc").load_from_scope().make_loader()
