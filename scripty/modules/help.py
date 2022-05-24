from __future__ import annotations

__all__: tuple[str, ...] = ("loader_help",)

import miru
import tanchi
import tanjun

import scripty


class HelpView(miru.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            miru.Button(
                label="Website",
                url="https://scriptybot.web.app/",
            )
        )
        self.add_item(
            miru.Button(
                label="Docs",
                url="https://scriptydev.github.io/prescripty/",
            )
        )
        self.add_item(
            miru.Button(
                label="Commands",
                url="https://scriptydev.github.io/prescripty/reference/",
            )
        )
        self.add_item(
            miru.Button(
                label="Invite",
                url=scripty.INVITE_URL,
            )
        )


@tanchi.as_slash_command("help")
async def help_(ctx: tanjun.abc.SlashContext) -> None:
    """Display the help interface"""
    view = HelpView()
    await ctx.respond(components=view.build())


loader_help = tanjun.Component(name="help").load_from_scope().make_loader()
