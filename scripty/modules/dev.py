import pathlib

import alluka
import tanjun

import scripty

component = tanjun.Component()


@component.with_command
@tanjun.with_owner_check(error_message=None)
@tanjun.with_argument("module")
@tanjun.as_message_command("load")
async def load(
    ctx: tanjun.abc.MessageContext,
    module: str,
    *,
    client: alluka.Injected[tanjun.Client],
) -> None:
    """Load module

    Parameters
    ----------
    module : str
        Module to load
    """
    await client.reload_modules_async(pathlib.Path(f"scripty/modules/{module}.py"))
    await ctx.respond(
        scripty.Embed(
            title="Load",
            description=f"`{module}` module loaded",
        )
    )


@component.with_command
@tanjun.with_owner_check(error_message=None)
@tanjun.with_argument("module")
@tanjun.as_message_command("reload")
async def reload(
    ctx: tanjun.abc.MessageContext,
    module: str,
    client: alluka.Injected[tanjun.Client],
) -> None:
    """Reload module

    Parameters
    ----------
    module : str
        Module to reload
    """
    await client.reload_modules_async(pathlib.Path(f"scripty/modules/{module}.py"))
    await ctx.respond(
        scripty.Embed(
            title="Load",
            description=f"`{module}` module reloaded",
        )
    )


@component.with_command
@tanjun.with_owner_check(error_message=None)
@tanjun.as_message_command("sync")
async def sync(
    ctx: tanjun.abc.MessageContext,
    client: alluka.Injected[tanjun.Client],
) -> None:
    """Sync global application commands"""
    await client.declare_global_commands()
    await ctx.respond(
        scripty.Embed(
            title="Sync",
            description="Successfully synced global application commands",
        )
    )


@component.with_command
@tanjun.with_owner_check(error_message=None)
@tanjun.with_argument("module")
@tanjun.as_message_command("unload")
async def unload(
    ctx: tanjun.abc.MessageContext,
    module: str,
    client: alluka.Injected[tanjun.Client],
) -> None:
    """Unload module

    Parameters
    ----------
    module : str
        Module to unload
    """
    client.unload_modules(pathlib.Path(f"scripty/modules/{module}.py"))
    await ctx.respond(
        scripty.Embed(
            title="Unload",
            description=f"`{module}` module unloaded",
        )
    )


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
