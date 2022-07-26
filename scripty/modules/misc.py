from __future__ import annotations

__all__: tuple[str, ...] = ("loader_misc",)

import hikari
import tanchi
import tanjun
from gpytranslate import Translator

from scripty.functions import embeds


@tanjun.as_user_menu("Avatar")
async def avatar(
    ctx: tanjun.abc.MenuContext, user: hikari.User | hikari.InteractionMember
) -> None:
    """Get user avatar"""
    await ctx.respond(
        embeds.Embed(title="Avatar")
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
            embeds.Embed(
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
        embeds.Embed(title="Translate")
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
    ctx: tanjun.abc.SlashContext,
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
        embeds.Embed(title="Translate")
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
    embed = embeds.Embed(title="Echo", description=f"```{text}```").set_author(
        name=str(ctx.author),
        icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
    )

    await ctx.respond(embed)


@tanchi.as_slash_command()
async def poll(
    ctx: tanjun.abc.SlashContext,
    topic: str,
    option_1: str,
    option_2: str,
    option_3: str | None = None,
    option_4: str | None = None,
    option_5: str | None = None,
    option_6: str | None = None,
    option_7: str | None = None,
    option_8: str | None = None,
    option_9: str | None = None,
    option_10: str | None = None,
) -> None:
    """Create a simple poll

    Parameters
    ----------
    topic : str
        Topic of the poll
    option_1 : str
        Option A
    option_2 : str
        Option B
    option_3 : str | None
        Option C
    option_4 : str | None
        Option D
    option_5 : str | None
        Option E
    option_6 : str | None
        Option F
    option_7 : str | None
        Option G
    option_8 : str | None
        Option H
    option_9 : str | None
        Option I
    option_10 : str | None
        Option J
    """
    options: dict[str, str | None] = {
        "1️⃣": option_1,
        "2️⃣": option_2,
        "3️⃣": option_3,
        "4️⃣": option_4,
        "5️⃣": option_5,
        "6️⃣": option_6,
        "7️⃣": option_7,
        "8️⃣": option_8,
        "9️⃣": option_9,
        "🔟": option_10,
    }

    embed = embeds.Embed(
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
