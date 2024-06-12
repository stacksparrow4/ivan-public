import re

import discord

import chat

from constants import BOT_TOKEN, COMMAND_PREFIX, WHITELISTED_CHANNELS

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

async def bot_reply(message, resp):
    emojified_resp = resp
    for emoji in message.guild.emojis:
        emojified_resp = emojified_resp.replace(f":{emoji.name}:", f"<:{emoji.name}:{emoji.id}>")

    if len(emojified_resp) > 1950:
        await message.reply(emojified_resp[:1950] + "...")
    else:
        await message.reply(emojified_resp)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.channel.id in WHITELISTED_CHANNELS:
        return
    
    parts = message.content.split(maxsplit=1)

    if len(parts) > 0 and parts[0] == COMMAND_PREFIX:
        async with message.channel.typing():
            if len(parts) == 1:
                await bot_reply(message, chat.generate_chat())
            else:
                prompt = parts[1]

                if prompt.endswith("..."):
                    prompt = prompt[:-3].rstrip()
                else:
                    prompt += "\n"
                
                prompt = re.sub(r"<(:[^:]+:)[0-9]+>", r"\1", prompt)

                resp = chat.complete(prompt)

                await bot_reply(message, resp)

client.run(BOT_TOKEN)
