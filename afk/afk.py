from typing import Dict, Optional, Set
from datetime import datetime
import discord
from redbot import VersionInfo, version_info
from redbot.core import Config, checks, commands
from redbot.core.bot import Red


class Afk(commands.Cog):
    "Afk cog which will make programmers break their tables and start drinking"
    __version__ = "0.0.1"
    __author__ = ["Demantom"]

    def __init__(self, bot):
        self.bot: Red = bot
        default_guild: Dict[str, Optional[int]] = {"mute_role": None}
        self.config.register_guild(**default_guild)
        self.config.register_guild(**self.default_guild_settings)
        self.config.register_user(**self.default_user_settings)
        self.config = Config.get_conf(self, force_registration=True)
    async def afk_settings(self, ctx):
        author = ctx.author
        msg = ""
        data = {
            "MESSAGE": "user is afk"

        }

    @commands.command(name="afk")
    async def afk_(self, ctx, delete_after: Optional[int] = None, *, message: str = None):
        """
            sets afk
        """
        if delete_after is not None and delete_after < 5:
            return await ctx.send("Please set a time longer than 5 seconds for the `delete_after` argument")

        author = ctx.message.author
        mess = await self.config.user(author).MESSAGE()
        if mess:
            await self.config.user(author).MESSAGE.set(False)
            msg = "You're now back."
        else:
            if message is None:
                await self.config.user(author).MESSAGE.set((" ", delete_after))
            else:
                await self.config.user(author).MESSAGE.set((message, delete_after))
            msg = "You're now set as afk."
        await ctx.send(msg)
