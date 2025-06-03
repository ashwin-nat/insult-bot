import discord
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!insult'):
        if not message.mentions:
            await message.channel.send("Please mention someone to insult. Usage: `!insult @username`")
            return

        # Get the first mentioned user
        target = message.mentions[0]
        target_name = target.display_name

        # Build API URL
        api_url = f'https://insult.mattbas.org/api/insult?who={target_name}'

        # Call the insult API
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    insult = await resp.text()
                    await message.channel.send(insult)
                else:
                    await message.channel.send("Useless MF shit API is not working")

client.run(TOKEN)