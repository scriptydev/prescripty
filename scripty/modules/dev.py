import asyncio
import pathlib

import hikari
import tanchi
import tanjun

import scripty


component = tanjun.Component()


# Not working currently 🤔
# async def set_dev_cmds(
#     client: tanjun.Client = tanjun.inject(type=tanjun.Client),
# ):
#     await client.declare_application_commands(
#         [load_, reload, unload_, sync], guild=scripty.GUILD_ID_PRIMARY
#     )


# loop = asyncio.get_event_loop()
# loop.create_task(set_dev_cmds())


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command("load", is_global=False)
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
    module = module.lower()

    await client.reload_modules_async(
        pathlib.Path(f"scripty/modules/{module}.py")
    )

    embed = hikari.Embed(
        title="Load",
        description=f"`{module}` module loaded",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed)


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command(is_global=False)
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
    module = module.lower()

    await client.reload_modules_async(
        pathlib.Path(f"scripty/modules/{module}.py")
    )

    embed = hikari.Embed(
        title="Load",
        description=f"`{module}` module reloaded",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed)


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command(is_global=False)
async def sync(
    ctx: tanjun.abc.SlashContext,
    client: tanjun.abc.Client = tanjun.inject(type=tanjun.abc.Client),
) -> None:
    """Sync global application commands"""
    await client.declare_global_commands()

    embed = hikari.Embed(
        title="Sync",
        description="Successfully synced global application commands",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed)


@component.with_command
@tanjun.with_owner_check
@tanchi.as_slash_command("unload", is_global=False)
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
    module = module.lower()

    client.unload_modules(pathlib.Path(f"scripty/modules/{module}.py"))

    embed = hikari.Embed(
        title="Load",
        description=f"`{module}` module unloaded",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed)


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
