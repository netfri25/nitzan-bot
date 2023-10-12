import os
from typing import List
from dotenv import load_dotenv
import random

from discord import Intents, Member, Client, Message

INTENTS = Intents(members=True, messages=True, message_content=True)
client: Client = Client(intents=INTENTS)

global all_curses
all_curses: List[str]

@client.event
async def on_ready() -> None:
    print(f"{client.user} is ready")


@client.event
async def on_member_join(member: Member) -> None:
    guild_channels = member.guild.text_channels
    if len(guild_channels) == 0:
        return
    channel = guild_channels[0]

    k = random.randrange(1, 10)
    curses = ', '.join(random.choices(all_curses, k=k))
    await channel.send(f"{member.mention} {curses}.")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return None


def main():
    global all_curses

    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        print("Please provide TOKEN in a .env file")
        exit(1)

    with open('curses.txt') as f:
        all_curses = list(map(str.strip, f.readlines()))

    client.run(TOKEN)

main()
