import discord
from discord.ext import commands
from config import TOKEN, intents
from database import init_db
from commands import task_commands, project_commands, user_commands, admin_commands
from listeners import message_listener, button_listener
from scheduler import reminder_scheduler

# Initialize database
init_db()

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Add command modules
bot.add_cog(task_commands.TaskCommands(bot))
bot.add_cog(project_commands.ProjectCommands(bot))
bot.add_cog(user_commands.UserCommands(bot))
bot.add_cog(admin_commands.AdminCommands(bot))

# Add listeners
@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')
    await reminder_scheduler.start_scheduler(bot)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await message_listener.handle_message(bot, message)
    await bot.process_commands(message)

@bot.event
async def on_interaction(interaction):
    await button_listener.handle_button_interaction(bot, interaction)

# Run bot
if __name__ == '__main__':
    bot.run(TOKEN)
