import os
import logging
import aiohttp
from urllib.parse import quote
from dotenv import load_dotenv
import discord

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Debug: Check if token is loaded
if not DISCORD_TOKEN:
    logger.error("DISCORD_TOKEN not found in environment variables!")
    logger.error("Make sure your .env file exists and contains DISCORD_TOKEN=your_token")
    exit(1)
else:
    logger.info("Discord token loaded successfully")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    if client.user is None:
        logger.error("Bot user is None after login - this should not happen")
        return

    logger.info(f'Bot logged in successfully as {client.user}')
    logger.info(f'Bot ID: {client.user.id}')
    logger.info(f'Connected to {len(client.guilds)} server(s)')
    for guild in client.guilds:
        logger.info(f'  - {guild.name} (ID: {guild.id})')

@client.event
async def on_message(message: discord.Message):
    # Don't respond to own messages
    if message.author == client.user:
        return

    # Debug: Print all messages
    logger.debug(f'Message from {message.author} in #{message.channel}: {message.content}')

    # Check for insult command
    if message.content.startswith('!insult'):
        logger.info(f"Insult command detected from {message.author}")

        # Parse the command to extract user name
        command_parts = message.content.split(' ', 1)  # Split only on first space

        if len(command_parts) < 2 or not command_parts[1].strip():
            # No user name provided
            await message.channel.send("Please provide a user name! Usage: `!insult <user_name>` or `!insult @user`")
            logger.info("No user name provided in insult command")
            return

        user_input = command_parts[1].strip()
        insult_name = user_input

        # Check if it's a mention and extract the actual username
        if user_input.startswith('<@') and user_input.endswith('>'):
            # Extract user ID from mention
            user_id_str = user_input[2:-1]
            if user_id_str.startswith('!'):  # Nickname mention format
                user_id_str = user_id_str[1:]

            try:
                user_id = int(user_id_str)
                target_user = None
                if message.guild:
                    try:
                        target_user = await message.guild.fetch_member(user_id)
                    except discord.NotFound:
                        logger.warning(f"User with ID {user_id} not found in guild.")
                    except discord.Forbidden:
                        logger.warning("Bot doesn't have permission to fetch members.")
                    except discord.HTTPException as e:
                        logger.error(f"HTTP error while fetching member: {e}")
                if target_user:
                    insult_name = target_user.display_name  # Use their display name
                    logger.info(f"Extracted username from mention: {insult_name}")
                else:
                    logger.warning(f"Could not find user with ID: {user_id}")
                    await message.channel.send("Could not find that user!")
                    return
            except ValueError:
                logger.warning(f"Invalid user ID in mention: {user_id_str}")
                await message.channel.send("Invalid user mention!")
                return

        logger.info(f"Using name for insult: '{insult_name}'")

        try:
            # Call the insult API with URL encoding to handle spaces
            async with aiohttp.ClientSession() as session:
                # URL encode the name to handle spaces and special characters
                encoded_name = quote(insult_name)
                api_url = f"https://insult.mattbas.org/api/insult?who={encoded_name}"
                logger.debug(f"Calling insult API: {api_url}")

                async with session.get(api_url) as response:
                    if response.status == 200:
                        insult_text = await response.text()
                        insult_text = insult_text.strip()  # Remove any extra whitespace
                        logger.info(f"Got insult from API: {insult_text}")

                        await message.channel.send(insult_text)
                        logger.info("Insult sent successfully")
                    else:
                        logger.error(f"Insult API returned status {response.status}")
                        await message.channel.send("Sorry, couldn't generate an insult right now. Try again later!")

        except aiohttp.ClientError as e:
            logger.error(f"Network error calling insult API: {e}")
            await message.channel.send("Sorry, couldn't connect to the insult service. Try again later!")
        except discord.errors.Forbidden:
            logger.error("No permission to send messages in this channel")
        except Exception as e:
            logger.error(f"Error sending message: {e}")

@client.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Discord error in {event}: {args}")

# Start the bot
try:
    logger.info("Starting Discord bot...")
    client.run(DISCORD_TOKEN)
except discord.errors.LoginFailure:
    logger.error("Invalid Discord token!")
except Exception as e:
    logger.error(f"Error starting bot: {e}")