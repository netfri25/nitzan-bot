import os
import random

from time import time
from typing import List, Any
from discord.utils import setup_logging
from dotenv import load_dotenv

import discord
from discord import Intents, Member, Message
from discord.abc import Messageable

_log = setup_logging()

class CustomClient(discord.Client):
    curses: List[str] = []
    last_curse_time: float = 0
    CURSE_DELTA_TIME = 3 * 60

    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)

        with open('curses.txt') as f:
            self.curses = list(map(str.strip, f.readlines()))

        _log.info('successfully loaded curses')

    async def send(self, to: Messageable, msg: str) -> Any:
        _log.info(f"sending {msg} to {to}")
        return await to.send(msg)

    async def on_ready(self) -> None:
        _log.info(f"{self.user} is ready")

    async def on_member_join(self, member: Member) -> None:
        guild_channels = member.guild.text_channels
        if len(guild_channels) == 0:
            return
        channel = guild_channels[0]

        k = random.randrange(1, 10)
        curses = ', '.join(set(random.choices(self.curses, k=k)))
        await self.send(channel, f"{member.mention} {curses}.")

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        now = time()
        if now - self.last_curse_time < self.CURSE_DELTA_TIME:
            return
        self.last_curse_time = now

        channel = message.channel
        curse = random.choice(self.curses)
        await self.send(channel, f"{message.author.mention} {curse}")


def main():
    global all_curses

    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        _log.error("Please provide TOKEN in a .env file")
        exit(1)
    INTENTS = Intents(members=True, messages=True, message_content=True)
    CustomClient(INTENTS).run(TOKEN, log_handler=None)


main()
