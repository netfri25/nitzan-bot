import os
import random

from time import time
from typing import List, Any
from discord.utils import setup_logging
from dotenv import load_dotenv

import discord
from discord import Intents, Member, Message, User
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
        _log.info(f"{member.name} joined the server")
        channel = member.guild.system_channel
        if channel is None:
            guild_channles = member.guild.text_channels
            if len(guild_channles) == 0:
                _log.error(f"no text channels found in guild {member.guild}")
                return
            channel = guild_channles[0]

        k = random.randrange(1, 10)
        curses = ', '.join(set(random.choices(self.curses, k=k)))
        await self.send(channel, f"{member.mention} {curses}.")

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        # curse mentions
        channel = message.channel
        for user in message.mentions:
            if user == self.user:
                continue
            await self.send_curse(user, channel)

        # auto cursing
        now = time()
        if now - self.last_curse_time < self.CURSE_DELTA_TIME:
            return
        self.last_curse_time = now
        await self.send_curse(message.author, channel)

    async def send_curse(self, user_to_mention: User | Member, channel: Messageable) -> None:
        curse = random.choice(self.curses)
        await self.send(channel, f"{user_to_mention.mention} {curse}")


def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        _log.error("Please provide TOKEN in a .env file")
        exit(1)
    INTENTS = Intents(members=True, messages=True, message_content=True, guilds=True)
    CustomClient(INTENTS).run(TOKEN, log_handler=None)


main()
