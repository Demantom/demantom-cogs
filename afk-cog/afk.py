from typing import Dict, Optional, Set
import discord
from redbot import VersionInfo, version_info
from redbot.core import Config, checks, commands
from redbot.core.bot import Red


class Afk(commands.cog):
    __version__ = "0.0.1"
    __author__ = ["Demantom"]

    def __init__(self, bot):
        self.bot: Red = bot
        default_guild: Dict[str, Optional[int]] = {"mute_role": None}
        self.config.register_guild(**default_guild)
