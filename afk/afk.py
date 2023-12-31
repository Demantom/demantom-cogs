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

    default_global_settings = {"ign_servers": []}
    default_guild_settings = {"TEXT_ONLY": False, "BLACKLISTED_MEMBERS": []}
    default_user_settings = {
        "MESSAGE": False,
    }
    def __init__(self, bot):
        self.bot: Red = bot
        self.config = Config.get_conf(self,8423491260, force_registration=True)
        default_guild: Dict[str, Optional[int]] = {"mute_role": None}
        self.config.register_guild(**default_guild)
        self.config.register_guild(**self.default_guild_settings)
        self.config.register_user(**self.default_user_settings)

    @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        guild = message.guild
        if not guild or not message.mentions or message.author.bot:
            return
        if not message.channel.permissions_for(guild.me).send_messages:
            return

        blocked_guilds = await self.config.ign_servers()
        guild_config = await self.config.guild(guild).all()
        for author in message.mentions:
            if (guild.id in blocked_guilds and not await self.is_mod_or_admin(author)) or author.id in guild_config[
                "BLACKLISTED_MEMBERS"]:
                continue
            user_data = await self.config.user(author).all()
            embed_links = message.channel.permissions_for(guild.me).embed_links

            away_msg = user_data["MESSAGE"]
            # Convert possible `delete_after` of < 5s of before PR#212
            if isinstance(away_msg, list) and away_msg[1] is not None and away_msg[1] < 5:
                await self.config.user(author).MESSAGE.set((away_msg[0], 5))
                away_msg = away_msg[0], 5
            if away_msg:
                if type(away_msg) in [tuple, list]:
                    # This is just to keep backwards compatibility
                    away_msg, delete_after = away_msg
                else:
                    delete_after = None
                if embed_links and not guild_config["TEXT_ONLY"]:
                    em = await self.make_embed_message(author, away_msg, "away")
                    await message.channel.send(embed=em, delete_after=delete_after)
                elif (embed_links and guild_config["TEXT_ONLY"]) or not embed_links:
                    msg = await self.make_text_message(author, away_msg, "away")
                    await message.channel.send(msg, delete_after=delete_after)
                continue
    @commands.command(name="afksettings", aliases=["afkset"])
    async def afk_settings(self, ctx):
        author = ctx.author
        msg = ""
        data = {
            "MESSAGE": "user is afk",
        }
        settings = await self.config.user(author).get_raw()
        for attr, name in data.items():
            if type(settings[attr]) in [tuple, list]:
                # This is just to keep backwards compatibility
                status_msg, delete_after = settings[attr]
            else:
                status_msg = settings[attr]
                delete_after = None
            if settings[attr] and len(status_msg) > 20:
                status_msg = status_msg[:20] + "..."
            if settings[attr] and len(status_msg) <= 1:
                status_msg = "True"
            if delete_after:
                msg += f"{name}: {status_msg} deleted after {delete_after}s\n"
            else:
                msg += f"{name}: {status_msg}\n"


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
