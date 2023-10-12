import os
from dotenv import load_dotenv

from discord import Intents, Member, Client, Message

load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Please provide TOKEN in a .env file")
    exit(1)

INTENTS = Intents(members=True, messages=True, message_content=True)
client = Client(intents=INTENTS)


@client.event
async def on_ready() -> None:
    print(f"{client.user} is ready")


@client.event
async def on_member_join(member: Member) -> None:
    guild_channels = member.guild.text_channels
    if len(guild_channels) == 0:
        return

    channel = guild_channels[0]
    await channel.send(f"{member.mention} יבן זונה יבן שרמוטה למה מי אתה חושב שאתה מי???")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return None


client.run(TOKEN)
