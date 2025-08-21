# main.py
import discord
from discord.ext import commands
from config import Config
import logging
import os

# Set up basic logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('psyflixs_staff_bot')

# Define intents
intents = discord.Intents.default()
intents.message_content = True # Required for on_message
intents.members = True # Potentially useful for future features

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    logger.info(f"Bot '{bot.user}' is connected and ready.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the workflow"))

    try:
        synced = await bot.tree.sync() # Sync slash commands
        logger.info(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        logger.error(f"Failed to sync slash commands: {e}")

async def load_cogs():
    """Load all cogs from the cogs directory."""
    cogs = [
        "cogs.task_management",
        "cogs.notifications",
        "cogs.timezone",
        "cogs.recruitment"
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"Loaded extension: {cog}")
        except Exception as e:
            logger.error(f"Failed to load extension {cog}: {e}")

# Run the bot
if __name__ == "__main__":
    if not Config.DISCORD_TOKEN:
        logger.critical("DISCORD_TOKEN not found in environment variables. Please set it in your .env file.")
        exit(1)
    bot.loop.create_task(load_cogs())
    bot.run(Config.DISCORD_TOKEN)
