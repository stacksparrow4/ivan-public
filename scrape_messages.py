import json

import discord

import util

from constants import SCRAPE_CHANNELS, BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guild_messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Starting pull...")

    msg_data = []

    users = {}

    for channel in SCRAPE_CHANNELS:
        async for msg in client.get_channel(channel).history(limit=None, oldest_first=True):
            msg_data.append({"author": msg.author.name, "content": msg.content, "time": msg.created_at.timestamp()})
            users[msg.author.name] = {
                "name": msg.author.display_name.replace(" ", "-"),
                "id": str(msg.author.id)
            }
    
    util.write_to_path("data/message-db.json", json.dumps(msg_data))
    util.write_to_path("data/users.json", json.dumps(users))

    print("Finished!")

    await client.close()

client.run(BOT_TOKEN)