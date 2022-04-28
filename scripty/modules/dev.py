import pathlib

import hikari
import tanchi
import tanjun

import scripty


component = tanjun.Component()


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command("load", default_to_ephemeral=True)
async def load_(
    ctx: tanjun.abc.SlashContext,
    module: str,
    client: tanjun.abc.Client = tanjun.inject(type=tanjun.abc.Client),
) -> None:
    """Load module

    Parameters
    ----------
    module : str
        Module to load
    """
    await client.reload_modules_async(
        pathlib.Path(f"scripty/modules/{module}.py")
    )

    embed = hikari.Embed(
        title="Load",
        description=f"`{module}` module loaded",
        color=scripty.Color.GRAY_EMBED.value,
    )

    await ctx.respond(embed)


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command(default_to_ephemeral=True)
async def reload(
    ctx: tanjun.abc.SlashContext,
    module: str,
    client: tanjun.abc.Client = tanjun.inject(type=tanjun.abc.Client),
) -> None:
    """Reload module

    Parameters
    ----------
    module : str
        Module to reload
    """
    await client.reload_modules_async(
        pathlib.Path(f"scripty/modules/{module}.py")
    )

    embed = hikari.Embed(
        title="Load",
        description=f"`{module}` module reloaded",
        color=scripty.Color.GRAY_EMBED.value,
    )

    await ctx.respond(embed)


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command(default_to_ephemeral=True)
async def sync(
    ctx: tanjun.abc.SlashContext,
    client: tanjun.abc.Client = tanjun.inject(type=tanjun.abc.Client),
) -> None:
    """Sync global application commands"""
    await client.declare_global_commands()

    embed = hikari.Embed(
        title="Sync",
        description="Successfully synced global application commands",
        color=scripty.Color.GRAY_EMBED.value,
    )

    await ctx.respond(embed)


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command("unload", default_to_ephemeral=True)
async def unload_(
    ctx: tanjun.abc.SlashContext,
    module: str,
    client: tanjun.abc.Client = tanjun.inject(type=tanjun.abc.Client),
) -> None:
    """Unload module

    Parameters
    ----------
    module : str
        Module to unload
    """
    client.unload_modules(pathlib.Path(f"scripty/modules/{module}.py"))

    embed = hikari.Embed(
        title="Load",
        description=f"`{module}` module unloaded",
        color=scripty.Color.GRAY_EMBED.value,
    )

    await ctx.respond(embed)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
