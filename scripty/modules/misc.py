import hikari
import tanchi
import tanjun

import scripty


component = tanjun.Component()


@component.with_command
@tanjun.as_user_menu("Avatar")
async def avatar(ctx: tanjun.abc.MenuContext, user: hikari.User | hikari.InteractionMember) -> None:
    """Get user avatar"""
    embed = hikari.Embed(
        title=f"Avatar",
        color=scripty.Color.GRAY_EMBED.value,
    )
    embed.set_author(name=str(user), icon=user.avatar_url or user.default_avatar_url)
    embed.set_image(user.avatar_url or user.default_avatar_url)

    await ctx.respond(embed)


@component.with_command
@tanjun.with_author_permission_check(hikari.Permissions.MANAGE_MESSAGES)
@tanchi.as_slash_command()
async def echo(ctx: tanjun.abc.SlashContext, text: str) -> None:
    """Repeats user input

    Parameters
    ----------
    text : str
        Text to repeat
    """
    embed = hikari.Embed(
        title="Echo",
        description=f"```{text}```",
        color=scripty.Color.GRAY_EMBED.value,
    )
    embed.set_author(
        name=str(ctx.author),
        icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
    )

    await ctx.respond(embed)


@component.with_command
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

    embed = hikari.Embed(
        title=topic,
        description="\n\n".join(f"{key} {value}" for key, value in options.items() if value is not None),
        color=scripty.Color.GRAY_EMBED.value,
    )
    embed.set_author(
        name=str(ctx.author),
        icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
    )

    await ctx.respond(embed)

    for key, value in options.items():
        if value is not None:
            response = await ctx.interaction.fetch_initial_response()
            await response.add_reaction(key)


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
